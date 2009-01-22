"""
This file was written by Jose Antonio Martin H. for the RL-Glue project.
you are allowed to use it (and see it) fully but subject to the next conditions

1. to not cause damage to any person
2. to not use it to earn money except when you give me the 50% 
3. to use it to produce a state of the art RL agent, if not, think a lot and then come back to write a super agent.

This code is a 'parser' for the RL-Glue 3.0 TaskSpec.
It does not make any duplication of information, that is, what you get is always a view of the original string.
This is not the classic state-machine or automata approach to parsing languages so in particular you will se that
the parser is robust to a big set of taskpec string malformations still getting the right information.


Last modifed 22-1-2009 by Jose Antonio Martin H.
Added enforced parsing error catching.
"""

import sys
try:
    import psyco
    psyco.full()
except ImportError:
    pass

class TaskSpecParser:
    """
       RL-Glue TaskSpec Sparser V3
    """
    w = ["VERSION","PROBLEMTYPE","DISCOUNTFACTOR", "OBSERVATIONS","ACTIONS","REWARDS","EXTRA"]
    v = ["INTS","DOUBLES","CHARCOUNT"]
    expected_version = "RL-Glue-3.0"
    valid            = True
    last_error       = ""
    
    def __init__(self,ts):
        self.ts = ts
        if self.expected_version != self.getVersion():                   
            print "Warning: TaskSpec Version is not "+self.expected_version+" but "+self.getVersion()
            self.valid = False

    def getVersion(self):        
        a = len(self.w[0])+1                
        return self.ts[a:self.ts.find(" ",a)] 

    def Validate(self):
        if not self.valid:
            print "Warning: TaskSpec String is invalid: "+self.last_error
            return False
        return True
    
    def getValue(self,i,ts,w):
        try:
            a = ts.index(w[i]) + len(w[i]) + 1
        except: #ValueError:
            #raise AttributeError("Malformed TaskSpec String: could not find the "+w[i]+" keyword")
            self.last_error = "could not find the "+w[i]+" keyword"
            print "Warning: Malformed TaskSpec String: " +self.last_error
            self.valid = False
            return ""
        b=None
        if (i+1)<len(w):
            try:
                b = ts.index(w[i+1])-1
            except: #ValueError:
                #raise AttributeError("Malformed TaskSpec String: could not find the "+w[i+1]+" keyword")
                self.last_error = "could not find the "+w[i+1]+" keyword"
                print "Warning: Malformed TaskSpec String: " +self.last_error
                self.valid = False
                return ""

        return ts[a:b]

    def getProblemType(self):
        if not self.Validate():
            return ""
        return self.getValue(1,self.ts,self.w)

    def getDiscountFactor(self):
        if not self.Validate():
            return ""
        return self.getValue(2,self.ts,self.w)

    def CompleteVars(self,str_in):
        if not self.Validate():
            return ""
        """ forces the vars to have ints doubles and charcount
        """
        if self.v[0] not in str_in:
            str_in = self.v[0]+" (0 0 0) " + str_in
        if self.v[2] not in str_in:
            str_in+=self.v[2]+" 0 "
        if self.v[1] not in str_in:
            i = str_in.find(self.v[2])
            str_in= str_in[0:i]+self.v[1]+" (0 0 0) "+str_in[i:]
        return str_in

    def getObservations(self):
        if not self.Validate():
            return ""
        str_o = self.getValue(3,self.ts,self.w)
        return self.CompleteVars(str_o)

    def getActions(self):
        if not self.Validate():
            return ""
        str_a = self.getValue(4,self.ts,self.w)
        return self.CompleteVars(str_a)

    def getReward(self):
        if not self.Validate():
            return ""
        return self.getValue(5,self.ts,self.w)

    def getExtra(self):
        if not self.Validate():
            return ""
        return self.getValue(6,self.ts,self.w)

    def getRange(self,str_input):
        if not self.Validate():
            return ""

        try:
            str_input = str_input.replace("UNSPEC","'UNSPEC'")
            str_input = str_input.replace("NEGINF","'NEGINF'")
            str_input = str_input.replace("POSINF","'POSINF'")
            str_input = str_input.replace(" ",",")
            r = eval(str_input)
            if len(r)==2:
                return [list(r)]

            out = r[0]*([[r[1],r[2]]])
            return out
        
        except:
            self.last_error = "error ocurred while parsing a Range in "+str_input
            print "Warning: Malformed TaskSpec String: " +self.last_error
            print sys.exc_info()
            self.valid = False
            return ""
            
        

    def getRewardRange(self):
        if not self.Validate():
            return ""
        str_reward = self.getReward()
        return self.getRange(str_reward)

    def getVarInfoRange(self,i,ts,w):
        self.Validate()
        a = ts.index(w[i])
        b = ts.index(w[i+1])+1
        return ts[a:b]

    def GetVarValue(self,i,str_o):
        if not self.Validate():
            return ""
        str_r = self.getValue(i,str_o,self.v)
        str_r = str_r.replace(") (",")#(")
        str_r = str_r.replace(")(",")#(")  # Ok I can parse it but this (there is no space between consecutiive ranges) should be checked since this means that the taskspec is malformed.
        parts = str_r.split("#")
        obs=[]
        for p in parts:
            obs.extend(self.getRange(p))
        return obs

    def getIntObservations(self):
        if not self.Validate():
            return ""
        return self.GetVarValue(0,self.getObservations())

    def getDoubleObservations(self):
        if not self.Validate():
            return ""
        return self.GetVarValue(1,self.getObservations())

    def getCharCountObservations(self):
        if not self.Validate():
            return ""
        str_o = self.getObservations()
        return int(self.getValue(2,str_o,self.v))

    def getIntActions(self):
        if not self.Validate():
            return ""
        return self.GetVarValue(0,self.getActions())

    def getDoubleActions(self):
        if not self.Validate():
            return ""
        return self.GetVarValue(1,self.getActions())

    def getCharCountActions(self):
        if not self.Validate():
            return ""
        str_a = self.getActions()
        return int(self.getValue(2,str_a,self.v))




def test():
    # you can cut the taskspec by the main words with new line
    ts= """VERSION RL-Glue-3.0 PROBLEMTYPE episodic DISCOUNTFACTOR 1 OBSERVATIONS INTS (3 0 1) DOUBLES (2 -1.2 0.5)(-.07 .07) CHARCOUNT 1024
         ACTIONS INTS (2 0 4) CHARCOUNT 1024 REWARDS (5.0 UNSPEC) EXTRA some other stuff goes here"""
    print ts
    print
    print
    
    TaskSpec = TaskSpecParser(ts)
    if TaskSpec.valid:
        print "======================================================================================================="
        print "Version: ["+TaskSpec.getVersion()+"]"
        print "ProblemType: ["+TaskSpec.getProblemType()+"]"
        print "DiscountFactor: ["+TaskSpec.getDiscountFactor()+"]"
        print "======================================================================================================="
        print "\t \t \t \t Observations"
        print "======================================================================================================="
        #print "Observations: ["+TaskSpec.getObservations()+"]"
        print "Integers:",TaskSpec.getIntObservations()
        print "Doubles: ",TaskSpec.getDoubleObservations()
        print "Chars:   ",TaskSpec.getCharCountObservations()
        print "======================================================================================================="
        print "\t \t \t \t Actions"
        print "======================================================================================================"
        #print "Actions: ["+TaskSpec.getActions()+"]"
        print "Integers:",TaskSpec.getIntActions()
        print "Doubles: ",TaskSpec.getDoubleActions()
        print "Chars:   ",TaskSpec.getCharCountActions()
        print "======================================================================================================="        
        #print "Reward :["+TaskSpec.getReward()+"]")
        print "Reward Range:",TaskSpec.getRewardRange()
        print "Extra: ["+TaskSpec.getExtra()+"]"
        print "remeber that by using len() you get the cardinality of lists!"
        print "Thus:"
        print "len(",TaskSpec.getDoubleObservations(),") ==> ",len(TaskSpec.getDoubleObservations())," Double Observations"
        
   
        



if __name__=="__main__":
    test()
    

