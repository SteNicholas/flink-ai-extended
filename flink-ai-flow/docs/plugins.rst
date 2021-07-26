 .. Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

 ..   http://www.apache.org/licenses/LICENSE-2.0

 .. Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.



Plugins
=======

AIFlow has a plugin manager built-in that can integrate external features to its core by simply dropping plugin files in the ``ai_flow_plugins`` folder.

The python modules in the ``ai_flow_plugins`` folder get imported, and **scheduler_plugins**,  **job_plugins** and **blob_manager_plugins**
get integrated to AIFlow's main plugin factories and become available for use.

What for?
---------

AIFlow offers a generic scheduler for scheduling the workflow and job. Different scheduler have different stacks and different needs. Using AIFlow
plugins can be a way for companies to customize their Scheduler to integrate their ecosystem.

Plugins can be used as an easy way to write, share and activate new sets of features. There's also a need for a set of more complex applications to interact
with different engine for various and blob storage.

Examples:

* A set of operations to schedule the workflow and job in the Airflow
* A set of operations for the engine job like python, Flink, Spark etc.
* A pair of resource upload/download to the storage including HDFS, OSS etc.
* ...

AIFlow introduces three types of Plugin, including scheduler plugin, job plugin and blob manager plugin:

* ``scheduler_plugins`` are different integrations with Scheduler like Airflow, Azkaban etc, which perform and schedule the user-defined workflow and job
    based on the ``ai_flow.plugins_interface.scheduler_interface.Scheduler`` interface.
* ``job_plugins`` are composed of ``ai_flow.plugins_interface.job_plugin_interface.JobPluginFactory``, that organize the ``ai_flow.translator.translator.JobGenerator``
   and ``ai_flow.plugins_interface.job_plugin_interface.JobController`` components to generate and control the corresponding job.
* ``blob_manager_plugins`` are designed to upload and download files and resources for an execution of workflow, whose blob storage could be local or remote
   like HDFS, OSS etc.

.. _scheduler-plugin-interface:

Scheduler Plugin Interface
---------

To create a scheduler plugin you will need to derive the``ai_flow.plugins_interface.scheduler_interface.Scheduler`` class and
reference the objects you want to plug into AIFlow. Here's what the class you need to derive looks like:


.. code-block:: python

    class Scheduler(ABC):

        def __init__(self, config: Dict):
            self._config = config

        @property
        def config(self):
            return self._config

        @abstractmethod
        def submit_workflow(self, workflow: Workflow, project_context: ProjectContext) -> WorkflowInfo:
            """
            Submit the workflow to scheduler.
            :param workflow: ai_flow.workflow.workflow.Workflow type.
            :param project_context: ai_flow.context.project_context.ProjectContext type.
            :return: The workflow information.
            """
            pass

        @abstractmethod
        def delete_workflow(self, project_name: Text, workflow_name: Text) -> WorkflowInfo:
            """
            Delete the workflow from scheduler.
            :param project_name: The project name.
            :param workflow_name: The workflow name.
            :return: The workflow information.
            """
            pass

        @abstractmethod
        def pause_workflow_scheduling(self, project_name: Text, workflow_name: Text) -> WorkflowInfo:
            """
            Make the scheduler stop scheduling the workflow.
            :param project_name: The project name.
            :param workflow_name: The workflow name.
            :return: The workflow information.
            """
            pass

        @abstractmethod
        def resume_workflow_scheduling(self, project_name: Text, workflow_name: Text) -> WorkflowInfo:
            """
            Make the scheduler resume scheduling the workflow.
            :param project_name: The project name.
            :param workflow_name: The workflow name.
            :return: The workflow information.
            """
            pass

        @abstractmethod
        def start_new_workflow_execution(self, project_name: Text, workflow_name: Text) -> Optional[WorkflowExecutionInfo]:
            """
            Make the scheduler new a workflow execution.
            :param project_name: The project name.
            :param workflow_name: The workflow name.
            :return: The workflow execution information.
            """
            pass

        @abstractmethod
        def stop_all_workflow_execution(self, project_name: Text, workflow_name: Text) -> List[WorkflowExecutionInfo]:
            """
            Stop all workflow execution of the workflow.
            :param project_name: The project name.
            :param workflow_name: The workflow name.
            :return: The workflow execution information.
            """
            pass

        @abstractmethod
        def stop_workflow_execution(self, workflow_execution_id: Text) -> Optional[WorkflowExecutionInfo]:
            """
            Stop the workflow execution by execution id.
            :param workflow_execution_id: The workflow execution id.
            :return: The workflow execution information.
            """
            pass

        @abstractmethod
        def get_workflow_execution(self, workflow_execution_id: Text) -> Optional[WorkflowExecutionInfo]:
            """
            Get the workflow execution information.
            :param workflow_execution_id: The workflow execution id.
            :return: The workflow execution information.
            """
            pass

        @abstractmethod
        def list_workflow_executions(self, project_name: Text, workflow_name: Text) -> List[WorkflowExecutionInfo]:
            """
            List all workflow executions by workflow name.
            :param project_name: The project name.
            :param workflow_name: The workflow name.
            :return: The workflow execution information.
            """
            pass

        @abstractmethod
        def start_job_execution(self, job_name: Text, workflow_execution_id: Text) -> JobExecutionInfo:
            """
            Make the scheduler start a new job execution.
            :param job_name: The job name.
            :param workflow_execution_id: The workflow execution id.
            :return: The job execution information.
            """
            pass

        @abstractmethod
        def stop_job_execution(self, job_name: Text, workflow_execution_id: Text) -> JobExecutionInfo:
            """
            Make the scheduler stop the job execution.
            :param job_name: The job name.
            :param workflow_execution_id: The workflow execution id.
            :return: The job execution information.
            """
            pass

        @abstractmethod
        def restart_job_execution(self, job_name: Text, workflow_execution_id: Text) -> JobExecutionInfo:
            """
            Make the scheduler restart a job execution. If job status is running, first stop the job and then start it.
            :param job_name: The job name.
            :param workflow_execution_id: The workflow execution id.
            :return: The job execution information.
            """
            pass

        @abstractmethod
        def get_job_executions(self, job_name: Text, workflow_execution_id: Text) -> List[JobExecutionInfo]:
            """
            Get the job execution information by job name.
            :param job_name: The job name.
            :param workflow_execution_id: The workflow execution id.
            :return: The job execution information.
            """
            pass

        @abstractmethod
        def list_job_executions(self, workflow_execution_id: Text) -> List[JobExecutionInfo]:
            """
            List the job execution information by the workflow execution id.
            :param workflow_execution_id: The workflow execution id.
            :return: The job execution information.
            """
            pass

You can derive the schedule plugin interface by inheritance (please refer to the ``ai_flow_plugins.scheduler_plugins.airflow_scheduler.AirFlowScheduler`` below).
In the implementation, all options have been defined as class attributes, but you can also define them as config if you need to perform additional configuration.

Make sure you configure the user-defined scheduler plugin implementation in ``scheduler.scheduler_class_name`` scheduler configuration of
``ai_flow.endpoint.server.server.AIFlowServer``.

.. _scheduler-plugin-example:

Scheduler Plugin Example
-------

The code below defines a scheduler plugin that injects a set of workflow and job scheduling definitions in Airflow, which contains ``notification_service_uri`` and ``airflow_deploy_path`` configuration items.

.. code-block:: python

    class AirFlowScheduler(Scheduler):
    """
    AirFlowScheduler is an implementation of a Scheduler interface based on AirFlow.
    AirFlowScheduler contains two configuration items:
    1. notification_service_uri: The address of NotificationService.
    2. airflow_deploy_path: AirFlow dag file deployment directory.
    """

    def __init__(self, config: Dict):
        if 'notification_service_uri' not in config:
            raise Exception('`notification_service_uri` option of scheduler config is not configured. '
                            'Please add the `notification_service_uri` option under `scheduler_config` option!')
        if 'airflow_deploy_path' not in config:
            raise Exception('`airflow_deploy_path` option of scheduler config is not configured. '
                            'Please add the `notification_service_uri` option under `airflow_deploy_path` option!')
        super().__init__(config)
        self.dag_generator = DAGGenerator()
        self._airflow_client = None

    @classmethod
    def airflow_dag_id(cls, namespace, workflow_name):
        return '{}.{}'.format(namespace, workflow_name)

    @classmethod
    def dag_id_to_namespace_workflow(cls, dag_id: Text):
        tmp = dag_id.split('.')
        return tmp[0], tmp[1]

    @classmethod
    def airflow_state_to_status(cls, state) -> status.Status:
        if State.SUCCESS == state:
            return status.Status.FINISHED
        elif State.FAILED == state:
            return status.Status.FAILED
        elif State.RUNNING == state:
            return status.Status.RUNNING
        elif State.KILLED == state or State.SHUTDOWN == state \
                or State.KILLING == state:
            # We map airflow state KILLING to KILLED in the assumption that KILLING is a transient state,
            # and it is the best we can do.
            return status.Status.KILLED
        else:
            return status.Status.INIT

    @classmethod
    def status_to_airflow_state(cls, status_: status.Status) -> Text:
        if status.Status.FINISHED == status_:
            return State.SUCCESS
        elif status.Status.FAILED == status_:
            return State.FAILED
        elif status.Status.RUNNING == status_:
            return State.RUNNING
        elif status.Status.KILLED == status_:
            return State.KILLED
        else:
            return State.NONE

    @classmethod
    def dag_exist(cls, dag_id):
        with create_session() as session:
            dag = session.query(DagModel).filter(DagModel.dag_id == dag_id).first()
            if dag is None:
                return False
            else:
                return True

    @property
    def airflow_client(self):
        if self._airflow_client is None:
            self._airflow_client = EventSchedulerClient(server_uri=self.config.get('notification_service_uri'),
                                                        namespace=SCHEDULER_NAMESPACE)
        return self._airflow_client

    def submit_workflow(self, workflow: Workflow, project_context: ProjectContext) -> WorkflowInfo:
        dag_id = self.airflow_dag_id(project_context.project_name, workflow.workflow_name)
        code_text = self.dag_generator.generate(workflow=workflow,
                                                project_name=project_context.project_name)
        deploy_path = self.config.get('airflow_deploy_path')
        if deploy_path is None:
            raise Exception("airflow_deploy_path config not set!")
        if not os.path.exists(deploy_path):
            os.makedirs(deploy_path)
        airflow_file_path = os.path.join(deploy_path,
                                         dag_id + '.py')
        if os.path.exists(airflow_file_path):
            os.remove(airflow_file_path)
        with NamedTemporaryFile(mode='w+t', prefix=dag_id, suffix='.py', dir='/tmp', delete=False) as f:
            f.write(code_text)
        shutil.move(f.name, airflow_file_path)
        self.airflow_client.trigger_parse_dag(airflow_file_path)
        return WorkflowInfo(namespace=project_context.project_name,
                            workflow_name=workflow.workflow_name,
                            properties={'dag_file': airflow_file_path})

    def delete_workflow(self, project_name: Text, workflow_name: Text) -> WorkflowInfo:
        dag_id = self.airflow_dag_id(project_name, workflow_name)
        deploy_path = self.config.get('airflow_deploy_path')
        if deploy_path is None:
            raise Exception("airflow_deploy_path config not set!")
        airflow_file_path = os.path.join(deploy_path,
                                         dag_id + '.py')
        if os.path.exists(airflow_file_path):
            os.remove(airflow_file_path)
            return WorkflowInfo(namespace=project_name,
                                workflow_name=workflow_name,
                                properties={'dag_file': airflow_file_path})
        else:
            return None

    def pause_workflow_scheduling(self, project_name: Text, workflow_name: Text) -> WorkflowInfo:
        dag_id = self.airflow_dag_id(project_name, workflow_name)
        DagModel.get_dagmodel(dag_id=dag_id).set_is_paused(is_paused=True)
        return WorkflowInfo(namespace=project_name, workflow_name=workflow_name)

    def resume_workflow_scheduling(self, project_name: Text, workflow_name: Text) -> WorkflowInfo:
        dag_id = self.airflow_dag_id(project_name, workflow_name)
        DagModel.get_dagmodel(dag_id=dag_id).set_is_paused(is_paused=False)
        return WorkflowInfo(namespace=project_name, workflow_name=workflow_name)

    def start_new_workflow_execution(self, project_name: Text, workflow_name: Text) -> Optional[WorkflowExecutionInfo]:
        dag_id = self.airflow_dag_id(project_name, workflow_name)
        deploy_path = self.config.get('airflow_deploy_path')
        if deploy_path is None:
            raise Exception("airflow_deploy_path config not set!")
        if not self.dag_exist(dag_id):
            return None
        context: ExecutionContext = self.airflow_client.schedule_dag(dag_id)
        with create_session() as session:
            dagrun = DagRun.get_run_by_id(session=session, dag_id=dag_id, run_id=context.dagrun_id)
            if dagrun is None:
                return None
            else:
                return WorkflowExecutionInfo(
                    workflow_info=WorkflowInfo(namespace=project_name, workflow_name=workflow_name),
                    workflow_execution_id=str(dagrun.id),
                    status=status.Status.INIT)

    def stop_all_workflow_execution(self, project_name: Text, workflow_name: Text) -> List[WorkflowExecutionInfo]:
        workflow_execution_list = self.list_workflow_executions(project_name, workflow_name)
        for we in workflow_execution_list:
            if we.status == status.Status.RUNNING:
                self.stop_workflow_execution(we.workflow_execution_id)
        return workflow_execution_list

    def stop_workflow_execution(self, workflow_execution_id: Text) -> Optional[WorkflowExecutionInfo]:
        with create_session() as session:
            dagrun = session.query(DagRun).filter(DagRun.id == int(workflow_execution_id)).first()
            if dagrun is None:
                return None
            project_name, workflow_name = self.dag_id_to_namespace_workflow(dagrun.dag_id)
            context: ExecutionContext = ExecutionContext(dagrun_id=dagrun.run_id)
            current_context = self.airflow_client.stop_dag_run(dagrun.dag_id, context)
            return WorkflowExecutionInfo(workflow_info=WorkflowInfo(namespace=project_name,
                                                                    workflow_name=workflow_name),
                                         workflow_execution_id=workflow_execution_id,
                                         status=status.Status.KILLED)

    def get_workflow_execution(self, workflow_execution_id: Text) -> Optional[WorkflowExecutionInfo]:
        with create_session() as session:
            dagrun = session.query(DagRun).filter(DagRun.id == int(workflow_execution_id)).first()
            if dagrun is None:
                return None
            else:
                status_ = self.airflow_state_to_status(dagrun.state)
                project_name, workflow_name = self.dag_id_to_namespace_workflow(dagrun.dag_id)
                return WorkflowExecutionInfo(workflow_info=WorkflowInfo(namespace=project_name,
                                                                        workflow_name=workflow_name),
                                             workflow_execution_id=workflow_execution_id,
                                             status=status_,
                                             start_date=str(datetime_to_int64(dagrun.start_date)),
                                             end_date=str(datetime_to_int64(dagrun.end_date))
                                             )

    def list_workflow_executions(self, project_name: Text, workflow_name: Text) -> List[WorkflowExecutionInfo]:
        dag_id = self.airflow_dag_id(project_name, workflow_name)
        with create_session() as session:
            dagrun_list = session.query(DagRun).filter(DagRun.dag_id == dag_id).all()
            if dagrun_list is None:
                return []
            else:
                result = []
                for dagrun in dagrun_list:
                    status_ = self.airflow_state_to_status(dagrun.state)
                    result.append(WorkflowExecutionInfo(workflow_info=WorkflowInfo(namespace=project_name,
                                                                                   workflow_name=workflow_name),
                                                        workflow_execution_id=str(dagrun.id),
                                                        status=status_,
                                                        start_date=str(datetime_to_int64(dagrun.start_date)),
                                                        end_date=str(datetime_to_int64(dagrun.end_date)),
                                                        ))
                return result

    def start_job_execution(self, job_name: Text, workflow_execution_id: Text) -> Optional[JobExecutionInfo]:
        with create_session() as session:
            dagrun = session.query(DagRun).filter(DagRun.id == int(workflow_execution_id)).first()
            if dagrun is None:
                return None
            if dagrun.state != State.RUNNING:
                raise Exception('execution: {} state: {} can not trigger job.'.format(workflow_execution_id,
                                                                                      dagrun.state))
            task = dagrun.get_task_instance(job_name, session)
            if task is None:
                return None
            if task.state in State.unfinished:
                raise Exception('job:{} state: {} can not start!'.format(job_name, task.state))
            self.airflow_client.schedule_task(dag_id=dagrun.dag_id,
                                              task_id=job_name,
                                              action=SchedulingAction.START,
                                              context=ExecutionContext(dagrun_id=dagrun.run_id))
            project_name, workflow_name = self.dag_id_to_namespace_workflow(dagrun.dag_id)
            return JobExecutionInfo(job_name=job_name,
                                    status=self.airflow_state_to_status(task.state),
                                    workflow_execution
                                    =WorkflowExecutionInfo(workflow_info=WorkflowInfo(namespace=project_name,
                                                                                      workflow_name=workflow_name),
                                                           workflow_execution_id=workflow_execution_id,
                                                           status=self.airflow_state_to_status(dagrun.state)))

    def stop_job_execution(self, job_name: Text, workflow_execution_id: Text) -> Optional[JobExecutionInfo]:
        with create_session() as session:
            dagrun = session.query(DagRun).filter(DagRun.id == int(workflow_execution_id)).first()
            if dagrun is None:
                return None
            task = dagrun.get_task_instance(job_name, session)
            if task is None:
                return None
            if task.state in State.finished:
                raise Exception('job:{} state: {} can not stop!'.format(job_name, task.state))
            else:
                self.airflow_client.schedule_task(dag_id=dagrun.dag_id,
                                                  task_id=job_name,
                                                  action=SchedulingAction.STOP,
                                                  context=ExecutionContext(dagrun_id=dagrun.run_id))
            project_name, workflow_name = self.dag_id_to_namespace_workflow(dagrun.dag_id)
            return JobExecutionInfo(job_name=job_name,
                                    status=self.airflow_state_to_status(task.state),
                                    workflow_execution
                                    =WorkflowExecutionInfo(workflow_info=WorkflowInfo(namespace=project_name,
                                                                                      workflow_name=workflow_name),
                                                           workflow_execution_id=workflow_execution_id,
                                                           status=self.airflow_state_to_status(dagrun.state)))

    def restart_job_execution(self, job_name: Text, workflow_execution_id: Text) -> Optional[JobExecutionInfo]:
        with create_session() as session:
            dagrun = session.query(DagRun).filter(DagRun.id == int(workflow_execution_id)).first()
            if dagrun is None:
                return None
            if dagrun.state != State.RUNNING:
                raise Exception('execution: {} state: {} can not trigger job.'.format(workflow_execution_id,
                                                                                      dagrun.state))
            task = dagrun.get_task_instance(job_name, session)
            if task is None:
                return None
            self.airflow_client.schedule_task(dag_id=dagrun.dag_id,
                                              task_id=job_name,
                                              action=SchedulingAction.RESTART,
                                              context=ExecutionContext(dagrun_id=dagrun.run_id))
            project_name, workflow_name = self.dag_id_to_namespace_workflow(dagrun.dag_id)
            return JobExecutionInfo(job_name=job_name,
                                    status=self.airflow_state_to_status(task.state),
                                    workflow_execution
                                    =WorkflowExecutionInfo(workflow_info=WorkflowInfo(namespace=project_name,
                                                                                      workflow_name=workflow_name),
                                                           workflow_execution_id=workflow_execution_id,
                                                           status=self.airflow_state_to_status(dagrun.state)))

    def get_job_executions(self, job_name: Text, workflow_execution_id: Text) -> List[JobExecutionInfo]:
        with create_session() as session:
            dagrun = session.query(DagRun).filter(DagRun.id == int(workflow_execution_id)).first()
            if dagrun is None:
                return None
            task_list = session.query(TaskExecution).filter(TaskExecution.dag_id == dagrun.dag_id,
                                                            TaskExecution.execution_date == dagrun.execution_date,
                                                            TaskExecution.task_id == job_name).all()
            if task_list is None:
                return []
            else:
                result = self.build_job_execution_info_list(dagrun, task_list)
                return result

    def build_job_execution_info_list(self, dagrun, task_list):
        project_name, workflow_name = self.dag_id_to_namespace_workflow(dagrun.dag_id)
        result = []
        for task in task_list:
            job = JobExecutionInfo(job_name=task.task_id,
                                   status=self.airflow_state_to_status(task.state),
                                   start_date=str(datetime_to_int64(task.start_date)),
                                   end_date=str(datetime_to_int64(task.end_date)),
                                   workflow_execution
                                   =WorkflowExecutionInfo(workflow_info=WorkflowInfo(namespace=project_name,
                                                                                     workflow_name=workflow_name),
                                                          workflow_execution_id=str(dagrun.id),
                                                          status=self.airflow_state_to_status(dagrun.state)))
            result.append(job)
        return result

    def list_job_executions(self, workflow_execution_id: Text) -> List[JobExecutionInfo]:
        with create_session() as session:
            dagrun = session.query(DagRun).filter(DagRun.id == int(workflow_execution_id)).first()
            if dagrun is None:
                return None
            task_list = session.query(TaskExecution).filter(TaskExecution.dag_id == dagrun.dag_id,
                                                            TaskExecution.execution_date == dagrun.execution_date).all()
            if task_list is None:
                return []
            else:
                result = self.build_job_execution_info_list(dagrun, task_list)
                return result

In the above example, you could configure the Airflow scheduler in ``scheduler.scheduler_class_name`` scheduler configuration as follows:

.. code-block:: yaml

    scheduler:
        scheduler_class_name: ai_flow_plugins.scheduler_plugins.airflow.airflow_scheduler.AirFlowScheduler
        scheduler_config:
            airflow_deploy_path: /root/airflow/dag
            notification_service_uri: localhost:50052

.. _job-plugin-interface:

Job Plugin Interface
---------

To create a job plugin you will need to derive the``ai_flow.plugins_interface.job_plugin_interface.JobPluginFactory`` class and
defines the implementation for the ``ai_flow.translator.translator.JobGenerator`` and ``ai_flow.plugins_interface.job_plugin_interface.JobController``.
Here's what the class you need to derive looks like:


.. code-block:: python

    class JobPluginFactory(object):

        @abstractmethod
        def job_type(self) -> Text:
            """
            :return: The job type.
            """
            pass

        @abstractmethod
        def get_job_generator(self) -> JobGenerator:
            """
            :return a JobGenerator which type is same with AbstractJobPluginFactory job_type.
            """
            pass

        @abstractmethod
        def get_job_controller(self) -> JobController:
            """
            :return a JobController which type is same with AbstractJobPluginFactory job_type.
            """
            pass

     class JobGenerator(ABC):
        """
        JobGenerator: Convert AISubGraph(ai_flow.ai_graph.ai_graph.AISubGraph) to Job(ai_flow.workflow.job.Job)
        """

        @abstractmethod
        def generate(self, sub_graph: AISubGraph, resource_dir: Text = None) -> Job:
            """
            Convert AISubGraph(ai_flow.ai_graph.ai_graph.AISubGraph) to Job(ai_flow.workflow.job.Job)
            :param sub_graph: An executable Graph composed of AINode and data edges with the same job configuration.
            :param resource_dir: Store the executable files generated during the generation process.
            :return: Job(ai_flow.workflow.job.Job)
            """
            pass

     class JobController(ABC):
        """
        Used for control an executable job to specific platform when it's scheduled to run in workflow scheduler.
        The controller is able to control the lifecycle of a workflow job. Users can also implement custom job controller
        with their own job type.
        """

        @abstractmethod
        def submit_job(self, job: Job, job_runtime_env: JobRuntimeEnv) -> JobHandle:
            """
            Submit an executable job to run.
            :param job_runtime_env: The job runtime environment. Type: ai_flow.runtime.job_runtime_env.JobRuntimeEnv
            :param job: A job object that contains the necessary information for an execution.
            :return job_handle: a job handle that maintain the handler of a job runtime.
            """
            pass

        @abstractmethod
        def stop_job(self, job_handle: JobHandle, job_runtime_env: JobRuntimeEnv):
            """
            Stop a ai flow job.
            :param job_runtime_env: The job runtime environment. Type: ai_flow.runtime.job_runtime_env.JobRuntimeEnv
            :param job_handle: The job handle that contains the necessary information for an execution.
            """
            pass

        @abstractmethod
        def cleanup_job(self, job_handle: JobHandle, job_runtime_env: JobRuntimeEnv):
            """
            Clean up temporary resources created during this execution.
            :param job_runtime_env: The job runtime environment. Type: ai_flow.runtime.job_runtime_env.JobRuntimeEnv
            :param job_handle: The job handle that contains the necessary information for an execution.
            """
            pass

        @abstractmethod
        def get_result(self, job_handle: JobHandle, blocking: bool = True) -> object:
            """
            Return the job result.
            :param job_handle: The job handle that contains the necessary information for an execution.
            :param blocking: blocking is true: Wait for the job to finish and return the result of the job.
                            blocking is false: If the job is running, return None.
                                            If the job is finish, return the result of job.
            """
            pass

        @abstractmethod
        def get_job_status(self, job_handle: JobHandle) -> Status:
            """
            Return the job status.
            """
            pass

You can implement the interfaces of job plugin by inheritance (please refer to the ``ai_flow_plugins.job_plugins.python.python_job_plugin.PythonJobPluginFactory``, ``ai_flow_plugins.job_plugins.python.python_job_plugin.PythonJobGenerator``
and ``ai_flow_plugins.job_plugins.python.python_job_plugin.PythonJobController``). In the implementation for Python engine, PythonJobGenerator generates the Python modules described by ``ai_flow_plugins.job_plugins.python.python_job_plugin.PythonJob``.
PythonJobController controls the Python job submission which returns the ``ai_flow_plugins.job_plugins.python.python_job_plugin.PythonJobHandle`` for the information of job and operations to stop and clean the corresponding Python job.

Make sure you specify the job plugin implementation type in ``[job_name].job_type`` workflow configuration and invoke the ``register_job_plugin_factory`` function to register the job plugin defined including the registration of PythonJobGenerator and
PythonJobController. For the Python job, you could configure the Python job type in ``[job_name].job_type`` workflow configuration as follows:

.. code-block:: yaml

    [job_name]:
        job_type: python

.. _blob-manager-plugin-interface:

Blob Manager Plugin Interface
---------

To create a blob manager plugin you will need to derive the``ai_flow.plugins_interface.blob_manager_plugin_interface.BlobManager`` class that
defines the upload, download and cleanup operation of project resource files. Here's what the class you need to derive looks like:


.. code-block:: python

    class BlobManager(ABC):
        """
        A BlobManager is responsible for uploading and downloading files and resource for an execution of an ai flow project.
        """
        def __init__(self, config: Dict):
            self.config = config

        @abstractmethod
        def upload_project(self, workflow_snapshot_id: Text, project_path: Text) -> Text:
            """
            upload a given project to blob server for remote execution.

            :param workflow_snapshot_id: It is the unique identifier for each workflow generation.
            :param project_path: the path of this project.
            :return the uri of the uploaded project file in blob server.
            """
            pass

        @abstractmethod
        def download_project(self, workflow_snapshot_id, remote_path: Text, local_path: Text = None) -> Text:
            """
            download the needed resource from remote blob server to local process for remote execution.

            :param workflow_snapshot_id: It is the unique identifier for each workflow generation.
            :param remote_path: The project package uri.
            :param local_path: Download file root path.
            :return Local project path.
            """
            pass

        def cleanup_project(self, workflow_snapshot_id, remote_path: Text):
            """
            clean up the project files downloaded or created during this execution.

            :param workflow_snapshot_id: It is the unique identifier for each workflow generation.
            :param remote_path: The project package uri.
            """
            pass

You can derive the interface of blog manager plugin by inheritance (please refer to the ``ai_flow_plugins.blob_manager_plugins.oss_blob_manager.OssBlobManager``). In the implementation for OSS storage,
OssBlobManager is an implementation of BlobManager based on the OSS file system, which contains ``access_key_id``, ``access_key_secret``, ``bucket``, ``local_repository`` configuration items of OSS.

Make sure you configure the blob manager plugin implementation in ``blob.blob_manager_class`` project configuration to specify the blob manager class and additional configurations. For the Local blob manager,
you could configure the ``ai_flow_plugins.blob_manager_plugins.local_blob_manager.LocalBlobManager`` in ``blob.blob_manager_class`` project configuration as follows:

.. code-block:: yaml

    blob:
        blob_manager_class: ai_flow_plugins.blob_manager_plugins.local_blob_manager.LocalBlobManager
