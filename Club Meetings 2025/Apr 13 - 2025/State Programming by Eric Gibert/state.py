"""
Class to manage states for simple automation
"""
class State:
    def __init__(self, initialState, defaultSate=None):
        """
        Usually only one object is created to manage the current state.
        :param initialState:
        :param defaultSate: default state upon timer completion. If not indicated, initialState is used instead
        """
        self.lastState, self.currentState = None, initialState
        self.defaultState = defaultSate or initialState
        self.firstTime = True  # set to True when changing state

    def __eq__(self, chkState):
        """
        Syntax sugar to check the current state
        :return: true if chkStats == current state
        """
        return chkState == self.currentState

    def changeToDefault(self, t=None):
        """
        Callback function to force the current state to the default state
        """
        self.changeTo(self.defaultState)

    def changeTo(self, newState):
        """
        Change the currentState to a new given state, saving current in last State
        """
        self.lastState = self.currentState
        self.currentState = newState
        self.firstTime = True  # change to True when changing state for first time entry action
        # print("State changes from", self.lastState, "to", self.currentState)

    def __str__(self):
        return(f"currentState:{self.currentState} /  lastState={self.lastState}")
