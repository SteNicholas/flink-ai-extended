# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import json
import os
import traceback
from subprocess import Popen
from typing import Text

from ai_flow.common.configuration import AIFlowConfiguration
from ai_flow.context.project_context import ProjectContext, build_project_context
from ai_flow.endpoint.server.workflow_proto_utils import workflow_to_proto, workflow_execution_to_proto, \
    workflow_execution_list_to_proto, job_to_proto, job_list_to_proto
from ai_flow.plugin_interface.blob_manager_interface import BlobConfig
from ai_flow.plugin_interface.blob_manager_interface import BlobManagerFactory
from ai_flow.plugin_interface.scheduler_interface import Scheduler, JobExecutionInfo, WorkflowExecutionInfo
from ai_flow.protobuf.message_pb2 import ResultProto, StatusProto
from ai_flow.protobuf.scheduling_service_pb2 import \
    (ScheduleWorkflowRequest,
     WorkflowInfoResponse,
     WorkflowExecutionRequest,
     WorkflowExecutionResponse,
     ListWorkflowExecutionResponse,
     ScheduleJobRequest,
     JobInfoResponse,
     ListJobInfoResponse)
from ai_flow.protobuf.scheduling_service_pb2_grpc import SchedulingServiceServicer
from ai_flow.runtime.job_runtime_util import prepare_job_runtime_env
from ai_flow.scheduler.scheduler_factory import SchedulerFactory
from ai_flow.util import json_utils
from ai_flow.workflow.workflow import Workflow
from ai_flow.workflow.workflow import WorkflowPropertyKeys


class SchedulerServiceConfig(AIFlowConfiguration):

    def __init__(self):
        super().__init__()
        self['scheduler_config'] = {}

    def repository(self):
        if 'repository' not in self:
            return '/tmp'
        else:
            return self['repository']

    def set_repository(self, value):
        self['repository'] = value

    def scheduler_class(self):
        if self.get('scheduler_class') is not None:
            return self.get('scheduler_class')
        else:
            return None

    def set_scheduler_class(self, value):
        self['scheduler_class'] = value

    def scheduler_config(self):
        if 'scheduler_config' not in self:
            return None
        return self['scheduler_config']

    def set_scheduler_config(self, value):
        self['scheduler_config'] = value


class SchedulerService(SchedulingServiceServicer):
    def __init__(self,
                 scheduler_service_config: SchedulerServiceConfig):
        self._scheduler_service_config = scheduler_service_config
        self._scheduler: Scheduler \
            = SchedulerFactory.create_scheduler(scheduler_service_config.scheduler_class(),
                                                scheduler_service_config.scheduler_config())

    # workflow interface
    def submitWorkflow(self, request, context):
        try:
            rq: ScheduleWorkflowRequest = request
            if rq.workflow_json is None or '' == rq.workflow_json:
                return WorkflowInfoResponse(result=ResultProto(status=StatusProto.ERROR,
                                                               error_message='workflow json is empty!'))
            workflow: Workflow = json_utils.loads(rq.workflow_json)
            raw_config = {}
            raw_config.update(workflow.properties[WorkflowPropertyKeys.BLOB])
            blob_config = BlobConfig(raw_config)
            blob_manager = BlobManagerFactory.create_blob_manager(blob_config.blob_manager_class(),
                                                                  blob_config.blob_manager_config())
            project_path: Text = blob_manager \
                .download_project(workflow_snapshot_id=workflow.workflow_snapshot_id,
                                  remote_path=workflow.project_uri,
                                  local_path=self._scheduler_service_config.repository())

            project_context: ProjectContext = build_project_context(project_path)
            project_name = project_context.project_name

            workflow_info = self._scheduler.submit_workflow(workflow, project_context)
            if workflow_info is None:
                return WorkflowInfoResponse(
                    result=ResultProto(status=StatusProto.ERROR,
                                       error_message='{}, {} do not exist!'.format(project_name,
                                                                                   workflow.workflow_name)))

            contains_occlum = False
            occlum_image_path = None
            occlum_instance = None
            python_path = []
            for job_config in workflow.workflow_config.job_configs.values():
                if 'occlum' in job_config.job_type:
                    contains_occlum = True
                    if 'occlum_image_path' in job_config.properties:
                        occlum_image_path = job_config.properties['occlum_image_path']
                        occlum_instance = os.path.abspath(os.path.dirname(occlum_image_path))
                        python_path.insert(0, project_context.get_workflow_path(workflow.workflow_name).replace(
                            occlum_image_path, ''))
                        python_path.insert(0, os.path.join(project_path, 'dependencies', 'python').replace(
                            occlum_image_path, ''))

                        prepare_job_runtime_env(workflow.workflow_snapshot_id, workflow.workflow_name, project_context,
                                                JobExecutionInfo(job_name=job_config.job_name,
                                                                 workflow_execution=WorkflowExecutionInfo(
                                                                     workflow_execution_id='',
                                                                     workflow_info=workflow_info)),
                                                project_context.project_path)

            if contains_occlum and occlum_instance is not None:
                with open(os.path.join(os.path.abspath(os.path.dirname(occlum_image_path)), 'Occlum.json'),
                          'r') as occlum_json:
                    occlum_config = json.load(occlum_json)
                    occlum_config['env']['default'].append("PYTHONPATH={}".format(':'.join(python_path)))
                    print(occlum_config['env']['default'])
                os.remove(os.path.join(os.path.abspath(os.path.dirname(occlum_image_path)), 'Occlum.json'))
                with open(os.path.join(os.path.abspath(os.path.dirname(occlum_image_path)), 'Occlum.json'),
                          'w') as occlum_json:
                    json.dump(occlum_config, occlum_json)

                print('cd {} && SGX_MODE={} occlum build'.format(occlum_instance, str(
                    os.environ['SGX_MODE']) if 'SGX_MODE' in os.environ else 'HW'))
                occlum_build = Popen('cd {} && SGX_MODE={} occlum build'.format(occlum_instance, str(
                    os.environ['SGX_MODE']) if 'SGX_MODE' in os.environ else 'HW'), shell=True)
                occlum_build.wait()
                print('cd {} && occlum stop'.format(occlum_instance))
                occlum_stop = Popen('cd {} && occlum stop'.format(occlum_instance), shell=True)
                occlum_stop.wait()
                print('cd {} && occlum start'.format(occlum_instance))
                occlum_start = Popen('cd {} && occlum start'.format(occlum_instance), shell=True)
                occlum_start.wait()
                print('cd {} && occlum exec /bin/run_flink_fish.sh jm'.format(occlum_instance))
                start_job_manager = Popen('cd {} && occlum exec /bin/run_flink_fish.sh jm'.format(occlum_instance),
                                          shell=True)
                start_job_manager.wait()
                print('cd {} && occlum exec /bin/run_flink_fish.sh tm'.format(occlum_instance))
                start_task_manager = Popen('cd {} && occlum exec /bin/run_flink_fish.sh tm'.format(occlum_instance),
                                           shell=True)
                start_task_manager.wait()

            return WorkflowInfoResponse(result=ResultProto(status=StatusProto.OK),
                                        workflow=workflow_to_proto(workflow_info))
        except Exception as err:
            return WorkflowInfoResponse(result=ResultProto(status=StatusProto.ERROR,
                                                           error_message=traceback.format_exc()))

    def deleteWorkflow(self, request, context):
        try:
            rq: ScheduleWorkflowRequest = request
            workflow_info = self._scheduler.delete_workflow(rq.namespace, rq.workflow_name)
            if workflow_info is None:
                return WorkflowInfoResponse(
                    result=ResultProto(status=StatusProto.ERROR,
                                       error_message='{} do not exist!'.format(rq.workflow_name)))
            return WorkflowInfoResponse(result=ResultProto(status=StatusProto.OK),
                                        workflow=workflow_to_proto(workflow_info))
        except Exception as err:
            return WorkflowInfoResponse(result=ResultProto(status=StatusProto.ERROR,
                                                           error_message=traceback.format_exc()))

    def pauseWorkflowScheduling(self, request, context):
        try:
            rq: ScheduleWorkflowRequest = request
            workflow_info = self._scheduler.pause_workflow_scheduling(rq.namespace, rq.workflow_name)
            if workflow_info is None:
                return WorkflowInfoResponse(
                    result=ResultProto(status=StatusProto.ERROR,
                                       error_message='{} do not exist!'.format(rq.workflow_name)))
            return WorkflowInfoResponse(result=ResultProto(status=StatusProto.OK),
                                        workflow=workflow_to_proto(workflow_info))
        except Exception as err:
            return WorkflowInfoResponse(result=ResultProto(status=StatusProto.ERROR,
                                                           error_message=traceback.format_exc()))

    def resumeWorkflowScheduling(self, request, context):
        try:
            rq: ScheduleWorkflowRequest = request
            workflow_info = self._scheduler.resume_workflow_scheduling(rq.namespace, rq.workflow_name)
            if workflow_info is None:
                return WorkflowInfoResponse(
                    result=ResultProto(status=StatusProto.ERROR,
                                       error_message='{} do not exist!'.format(rq.workflow_name)))
            return WorkflowInfoResponse(result=ResultProto(status=StatusProto.OK),
                                        workflow=workflow_to_proto(workflow_info))
        except Exception as err:
            return WorkflowInfoResponse(result=ResultProto(status=StatusProto.ERROR,
                                                           error_message=traceback.format_exc()))

    def getWorkflow(self, request, context):
        return WorkflowInfoResponse(result=ResultProto(status=StatusProto.ERROR,
                                                       error_message='Do not support getWorkflow'))

    def listWorkflows(self, request, context):
        return WorkflowInfoResponse(result=ResultProto(status=StatusProto.ERROR,
                                                       error_message='Do not support listWorkflows'))

    # workflow execution interface

    def startNewWorkflowExecution(self, request, context):
        try:
            rq: WorkflowExecutionRequest = request
            workflow_execution = self._scheduler.start_new_workflow_execution(rq.namespace, rq.workflow_name)
            if workflow_execution is None:
                return WorkflowInfoResponse(
                    result=ResultProto(status=StatusProto.ERROR,
                                       error_message='{}, {} do not exist!'.format(rq.namespace, rq.workflow_name)))
            return WorkflowExecutionResponse(result=ResultProto(status=StatusProto.OK),
                                             workflow_execution=workflow_execution_to_proto(workflow_execution))
        except Exception as err:
            return WorkflowExecutionResponse(result=ResultProto(status=StatusProto.ERROR,
                                                                error_message=traceback.format_exc()))

    def killAllWorkflowExecutions(self, request, context):
        try:
            rq: WorkflowExecutionRequest = request
            workflow_execution_list = self._scheduler.stop_all_workflow_execution(rq.namespace, rq.workflow_name)
            response = ListWorkflowExecutionResponse(result=ResultProto(status=StatusProto.OK))
            response.workflow_execution_list.extend(workflow_execution_list_to_proto(workflow_execution_list))
            return response
        except Exception as err:
            return ListWorkflowExecutionResponse(result=ResultProto(status=StatusProto.ERROR,
                                                                    error_message=traceback.format_exc()))

    def killWorkflowExecution(self, request, context):
        try:
            rq: WorkflowExecutionRequest = request
            workflow_execution = self._scheduler.stop_workflow_execution(rq.execution_id)
            if workflow_execution is None:
                return WorkflowExecutionResponse(
                    result=ResultProto(status=StatusProto.ERROR,
                                       error_message='{} do not exist!'.format(rq.execution_id)))
            return WorkflowExecutionResponse(result=ResultProto(status=StatusProto.OK),
                                             workflow_execution=workflow_execution_to_proto(workflow_execution))
        except Exception as err:
            return WorkflowExecutionResponse(result=ResultProto(status=StatusProto.ERROR,
                                                                error_message=traceback.format_exc()))

    def getWorkflowExecution(self, request, context):
        try:
            rq: WorkflowExecutionRequest = request
            workflow_execution = self._scheduler.get_workflow_execution(rq.execution_id)
            if workflow_execution is None:
                return WorkflowExecutionResponse(
                    result=ResultProto(status=StatusProto.ERROR,
                                       error_message='{} do not exist!'.format(rq.execution_id)))
            return WorkflowExecutionResponse(result=ResultProto(status=StatusProto.OK),
                                             workflow_execution=workflow_execution_to_proto(workflow_execution))
        except Exception as err:
            return WorkflowExecutionResponse(result=ResultProto(status=StatusProto.ERROR,
                                                                error_message=traceback.format_exc()))

    def listWorkflowExecutions(self, request, context):
        try:
            rq: WorkflowExecutionRequest = request
            workflow_execution_list = self._scheduler.list_workflow_executions(rq.namespace, rq.workflow_name)
            response = ListWorkflowExecutionResponse(result=ResultProto(status=StatusProto.OK))
            response.workflow_execution_list.extend(workflow_execution_list_to_proto(workflow_execution_list))
            return response
        except Exception as err:
            return ListWorkflowExecutionResponse(result=ResultProto(status=StatusProto.ERROR,
                                                                    error_message=traceback.format_exc()))

    # job interface
    def startJob(self, request, context):
        try:
            rq: ScheduleJobRequest = request
            job = self._scheduler.start_job_execution(rq.job_name, rq.execution_id)
            if job is None:
                return JobInfoResponse(
                    result=ResultProto(status=StatusProto.ERROR,
                                       error_message='{} do not exist!'.format(rq.job_name)))
            return JobInfoResponse(result=ResultProto(status=StatusProto.OK), job=job_to_proto(job))
        except Exception as err:
            return JobInfoResponse(result=ResultProto(status=StatusProto.ERROR,
                                                      error_message=traceback.format_exc()))

    def stopJob(self, request, context):
        try:
            rq: ScheduleJobRequest = request
            job = self._scheduler.stop_job_execution(rq.job_name, rq.execution_id)
            if job is None:
                return JobInfoResponse(
                    result=ResultProto(status=StatusProto.ERROR,
                                       error_message='{} do not exist!'.format(rq.job_name)))
            return JobInfoResponse(result=ResultProto(status=StatusProto.OK), job=job_to_proto(job))
        except Exception as err:
            return JobInfoResponse(result=ResultProto(status=StatusProto.ERROR,
                                                      error_message=traceback.format_exc()))

    def restartJob(self, request, context):
        try:
            rq: ScheduleJobRequest = request
            job = self._scheduler.restart_job_execution(rq.job_name, rq.execution_id)
            if job is None:
                return JobInfoResponse(
                    result=ResultProto(status=StatusProto.ERROR,
                                       error_message='{} do not exist!'.format(rq.job_name)))
            return JobInfoResponse(result=ResultProto(status=StatusProto.OK), job=job_to_proto(job))
        except Exception as err:
            return JobInfoResponse(result=ResultProto(status=StatusProto.ERROR,
                                                      error_message=traceback.format_exc()))

    def getJob(self, request, context):
        try:
            rq: ScheduleJobRequest = request
            jobs = self._scheduler.get_job_executions(rq.job_name, rq.execution_id)
            if jobs is None:
                return JobInfoResponse(
                    result=ResultProto(status=StatusProto.ERROR,
                                       error_message='{} do not exist!'.format(rq.job_name)))
            return JobInfoResponse(result=ResultProto(status=StatusProto.OK), job=job_to_proto(jobs[0]))
        except Exception as err:
            return JobInfoResponse(result=ResultProto(status=StatusProto.ERROR,
                                                      error_message=traceback.format_exc()))

    def listJobs(self, request, context):
        try:
            rq: ScheduleJobRequest = request
            job_list = self._scheduler.list_job_executions(rq.execution_id)
            response = ListJobInfoResponse(result=ResultProto(status=StatusProto.OK))
            response.job_list.extend(job_list_to_proto(job_list))
            return response
        except Exception as err:
            return ListJobInfoResponse(result=ResultProto(status=StatusProto.ERROR,
                                                          error_message=traceback.format_exc()))
