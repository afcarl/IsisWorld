from pandac.PandaModules import ClockObject

class ScenarioException(Exception):    
    def __init__(self):
        return


class IsisTask(object):
    def __init__(self,scenario):
        self.description = None
        self._GlobalClock = ClockObject.getGlobalClock()
        self._scenario = scenario 

    def executeTaskCode(self,name,ref):
        """ Executes the task method"""
        exec ref.__code__ in {'task':self, 't':self}  # maps all mentions of 'task' to the self object.
        if not hasattr(self,'name'):
            self.name = name
    
    def startTask(self, captureMovie):
        def simulationTask(self, task):
            
            for agent in self.agents:
                agent.update(dt) 

    def getDescription(self):
        """ Builds the string that is presented in the Task GUI"""
        s = "<b>Task</b>: %s" % self.name
        if self.description != None:
            s += self.description
        s += "Created by: %s" % self._scenario.author 
        return s

    def _advanceTask(self, task):
        """ This method is added to Panda's task management and executed at each cycle
        whenever a task is running.  It checks to see if it's in training or testing mode. 
        This is responsible for saving screenshots at various intervals."""
        dt = self._GlobalClock.getDt()
        return task.cont
        
        

class IsisScenario(object):
    def __init__(self,name):
        # _taskDict stores a mapping of task names to task methods
        self._taskDict = {}
        self.name = name
        self.description = "No description"
        self.author = "Unknown"
        self._loadTaskFile(self.name)
        # envDict stores a mapping of variable names to isisObject and isisAgent instances
        self.envDict = {}
    
    
    def _loadTaskFile(self,fileName):
        print "Loading: %s" % fileName
        execfile("scenarios/%s.py" % fileName,{'scenario':self, 's':self},self.__dict__)
        # load all of the tasks
        task_functions =  filter(lambda x: x[0:4] == "task",dir(self))
        for tf in task_functions:    
            new_task = IsisTask(self)
            new_task.executeTaskCode(tf,self.__dict__[tf])
            # add the task to the dictionary
            self._taskDict[new_task.name] = new_task

    def getTaskByName(self,taskName):
        return self._taskDict[taskName]
            
    def getTaskList(self):
        return self._taskDict.keys()
