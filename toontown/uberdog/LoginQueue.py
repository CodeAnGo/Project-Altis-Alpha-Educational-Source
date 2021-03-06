
class LoginQueue(object):
    __slots__ = (
        '_csm', '_maxCapacity', '_id', '_queued', '_waiting')

    def __init__(self, csm, maxCapacity=15):
        self._csm = csm
        self._maxCapacity = maxCapacity
        self._id = 0
        self._queued = {}
        self._waiting = {}

    def getNewId(self):
        self._id += 1; return self._id

    def start(self):
        taskMgr.add(self.run, 'run-queue')

    def run(self, task):
        if not len(self._queued.keys()):
            return task.cont

        # if any requests are pending, add them and handle there request
        for id in self._waiting.keys():
            if not self.canQueue():
                break

            self._queued[id] = self._waiting.pop(id)

        for id in self._queued.keys():
            args = self._queued[id]

            # remove id from queued
            del self._queued[id]

            # call perform login function on csm
            self._csm.performLogin(*args)

        return task.cont

    def canQueue(self):
        return True if len(self._queued.keys()) < self._maxCapacity else False

    def queueObject(self, id, args):
        if self.canQueue():
            self._queued[id] = args
        else:
            self._waiting[id] = args
