
#import  libraries
from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from mesa import Agent, Model
from mesa.time import RandomActivation
import math
import matplotlib.pyplot as plt
import numpy as np




#creating the agent class
class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.gender = -1
        self.salary = 100000
        self.current_year = 2
        self.entry_year = 1
        self.exit_year=0
        self.rank = 1

    #this function receives a random Professor, increases their salary and also their rank   
    def step(self):
        self.salary +=3000
        if (self.current_year- self.entry_year)%6==0:
            self.rank +=1
        self.current_year+=1
        # print ("Hi, I am Professsor " + str(self.unique_id) +"." + " and my salary is " + str(self.salary)+" my rank:"+  str(self.rank) + " my gender:" + str(self.gender))

#creating model class that contains professors       
class MoneyModel(Model):
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.active_professor = []
        self.quit_request = []
        self.quited_professors = []
        self.prof_incom = []
        self.male_professor_incom = []
        self.female_professor_incom = []
        
        # Create agents, 40% female and 60%male and add them to an array 
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            if i<=(math.floor(self.num_agents*.4)):
                a.gender = 0
            elif i>=(math.floor(self.num_agents*.4)):
                a.gender = 1
            self.active_professor.append(a)

        
        #adding array to the schedule 
        for each in self.active_professor:
            self.schedule.add(each)

    def average(self,lst):
        return sum(lst) / len(lst)

    #this functin does some orders in each step. Here each step is each year
    def step(self):
    
        
        '''creating 4 random professors who want to quit each year'''
        self.quit_request= random.sample(range(1, (len(self.active_professor))), 4)
        
        #start the step and schedule 
        self.schedule.step()

        #deleting professors from active list and add a new on with the gender of deleted one to the list of active professors
        for each in self.quit_request:
            temp = self.active_professor[each]
            self.last_id = self.active_professor[-1].unique_id
            self.active_professor.pop(each)
            self.schedule.remove(temp)
            self.quited_professors.append(temp)
            self.new_hired_prof = MoneyAgent(self.last_id+1,self)
            self.new_hired_prof.gender = temp.gender
            self.active_professor.append(self.new_hired_prof)
            self.schedule.add(self.new_hired_prof)


        


        #30% of professors should receive special increase 
        special_increase = random.sample(range(self.num_agents), int(self.num_agents*.3))

        #10% of professors should receive 1500$ increase
        for each in range(int(math.floor(special_increase.__len__()/3))):
            self.active_professor[each].salary +=1500

        #10% of professors should receive 3000 increase
        for each in range(math.floor(special_increase.__len__()/3), math.floor((special_increase.__len__()*2)/3)):
            
            self.active_professor[each].salary +=3000

        #10% of professors should receive 6000 increase
        for each in range(math.floor((special_increase.__len__()*2)/3), special_increase.__len__()):
            self.active_professor[each].salary += 6000


        # for each_prof in self.quited_professors:
            # print("I resigned",each_prof.unique_id," with salary:",each_prof.salary, "gender:" , each_prof.gender )

        for each in self.active_professor:
            self.prof_incom.append(each.salary)
            if each.gender ==0:
                self.female_professor_incom.append(each.salary)
            elif each.gender==1:
                self.male_professor_incom.append(each.salary) 
        

       

#creating a MoneyModel object
model = MoneyModel(240)

# creating a list to save average salary of whole group, female professors and male professors EACH YEAR
average_salary_of_whole_group_each_year = []
average_salary_of_whole_male_group_each_year= []
average_salary_of_whole_female_group_each_year= []


# creating a list to save average salary of whole group, female professors and male professors during the WHOLE GROUP
sum_of_income_each_year = []
sum_of_male_income_each_year = []
sum_of_female_income_each_year = []


#starting the simulation 
for i in range(100):
    # print("year "+str(i))
    model.step()
    average_salary_of_whole_group_each_year.append(sum(model.prof_incom)/len(model.prof_incom))
    sum_of_income_each_year.append(sum(model.prof_incom))
    average_salary_of_whole_male_group_each_year.append(sum(model.male_professor_incom)/len(model.male_professor_incom))
    sum_of_male_income_each_year.append(sum(model.male_professor_incom))
    average_salary_of_whole_female_group_each_year.append(sum(model.female_professor_incom)/len(model.female_professor_incom))
    sum_of_female_income_each_year.append(sum(model.female_professor_incom))



#plot for the average of income of whole group
figure1 = plt.figure(1)
plt.plot(list(range(1,101)),average_salary_of_whole_group_each_year,label="Whole Group")
#plot for the average of female professor's income
plt.plot(list(range(1,101)),average_salary_of_whole_female_group_each_year,label="Female Group")
#plot for the average of male professor's income
plt.plot(list(range(1,101)),average_salary_of_whole_male_group_each_year,label="Male Group")
plt.xlabel("year")
plt.ylabel("Average Income of Various Group Each Year")
plt.legend()
figure1.show()



# plot for the average of whole group, male professors, female professor's income for the whole years
figure2 = plt.figure(2)
labels = ['Whole Goup', 'Female', 'Male']
whole_group_avrg = [sum(sum_of_income_each_year)/len(sum_of_income_each_year)]
men_group_avrg = [sum(sum_of_male_income_each_year)/len(sum_of_male_income_each_year)]
women_group_Avrg = [sum(sum_of_female_income_each_year)/len(sum_of_female_income_each_year)]

y_value = [whole_group_avrg[0],men_group_avrg[0],women_group_Avrg[0]]
y_pos = np.arange(len(labels))
plt.xticks(y_pos,labels)
plt.title("The Average of income-Whole Years")
plt.ylabel("Income")
plt.bar(y_pos,y_value)
figure2.show()


input()