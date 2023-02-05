'''
Hamza Naciri
Nour El Houda Sifeddine
Brahim Anegdouil

This code has been written in the context of a redaction of a research article about game theory in cybersecurity by our group. Please do not copy our code.
'''
import random
from statsmodels.stats.weightstats import ztest
import numpy
from scipy import stats

###############################################################################ASYMMETRIC GAME########################################################################################################

p_critical = 0.01 #Probability of bug hunter finding a critical vulnerability

p_high = 0.05 #Probability of bug hunter finding a high severity vulnerability

p_medium = 0.09 #Probability of bug hunter finding a medium severity vulnerability

p_low = 0.99 #Probability of bug hunter finding a low severity vulnerability

bug_hunter_payoff_critical = 10000 #Payoff for bug hunter if they find a critical vulnerability

bug_hunter_payoff_high = 5000 #Payoff for bug hunter if they find a high severity vulnerability

bug_hunter_payoff_medium = 1000 #Payoff for bug hunter if they find a medium severity vulnerability

bug_hunter_payoff_low = 500 #Payoff for bug hunter if they find a low severity vulnerability

bug_hunter_payoff_none = 0 #Payoff for bug hunter if they don't find any vulnerabilities

bug_hunter_cost = 100 #Cost for bug hunter to perform the pentest

patch_cost_critical = 5000 #Cost for defender to pay for patch for a critical vulnerability

patch_cost_high = 2500 #Cost for defender to pay for patch for a high severity vulnerability

patch_cost_medium = 1000 #Cost for defender to pay for patch for a medium severity vulnerability

patch_cost_low = 500 #Cost for defender to pay for patch for a low severity vulnerability

p_defender_success = 0.7 #Probability of defender successfully patching a vulnerability

p_none = 0.375 #Probability of bug hunter finding no vulnerabilities

p_already_reported = 0.375 #Probability of bug hunter finding a vulnerability that has already been reported

#Total number of rounds to play
num_rounds = 150
mean_payoff_bug_hunter = 0
mean_payoff_defender = 0

bug_hunter_payoff=0

defender_payoff=0

#Arrays for the samples
bug_hunter_array = numpy.array([])
defender_array = numpy.array([])

for i in range(num_rounds):
    # try your luck and find a vulnerability
    luck = random.random()
    if luck < p_none:
        #Bug hunter finds no vulnerabilities
        severity = "none"
        bug_hunter_payoff += bug_hunter_payoff_none - bug_hunter_cost
        patch_cost = 0
        bug_hunter_array = numpy.append(bug_hunter_array, bug_hunter_cost)
        defender_array = numpy.append(defender_array, 0)
    elif luck < p_none + p_already_reported:
        #Bug hunter finds a vulnerability that has already been reported
        severity = "already reported"
        bug_hunter_payoff = bug_hunter_payoff + bug_hunter_payoff_none - bug_hunter_cost
        patch_cost = 0
        bug_hunter_array = numpy.append(bug_hunter_array, bug_hunter_cost)
        defender_array = numpy.append(defender_array, 0)
    elif luck < p_none + p_already_reported + p_critical:
        severity = "critical"
        bug_hunter_payoff += bug_hunter_payoff_critical
        patch_cost = -patch_cost_critical
        bug_hunter_array = numpy.append(bug_hunter_array, bug_hunter_payoff_critical)
        defender_array = numpy.append(defender_array, -patch_cost_critical)
    elif luck < p_none + p_already_reported + p_critical + p_high:
        severity = "high"
        bug_hunter_payoff += bug_hunter_payoff_high
        patch_cost = -patch_cost_high
        bug_hunter_array = numpy.append(bug_hunter_array, bug_hunter_payoff_high)
        defender_array = numpy.append(defender_array, -patch_cost_high)
    elif luck < p_none + p_already_reported + p_critical + p_high + p_medium:
        severity = "medium"
        bug_hunter_payoff += bug_hunter_payoff_medium
        patch_cost = -patch_cost_medium
        bug_hunter_array = numpy.append(bug_hunter_array, bug_hunter_payoff_medium)
        defender_array = numpy.append(defender_array, -patch_cost_medium)
    else:
        severity = "low"
        bug_hunter_payoff += bug_hunter_payoff_low
        patch_cost = -patch_cost_low
        bug_hunter_array = numpy.append(bug_hunter_array, bug_hunter_payoff_low)
        defender_array = numpy.append(defender_array, -patch_cost_low)
    
    #Defender attempts to patch the vulnerability
    if (severity != "none" or severity != "already reported") and random.random() < p_defender_success:
        # Defender successfully patches the vulnerability
        bug_hunter_payoff += 0
        defender_payoff += patch_cost
    else:
        #Defender fails to patch the vulnerability or there is no vulnerability to patch
        bug_hunter_payoff -= bug_hunter_cost
        defender_payoff += patch_cost
    
    print(f"Round {i+1}: Bug hunter finds {severity} vulnerability, Bug hunter payoff = {bug_hunter_payoff}, Defender payoff = {defender_payoff}")
print(f"Round {i+1}: Bug hunter finds {severity} vulnerability, Bug hunter payoff = {bug_hunter_payoff}, Defender payoff = {defender_payoff}")
mean_payoff_bug_hunter = bug_hunter_payoff/num_rounds
mean_payoff_defender = defender_payoff/num_rounds
print("Initial average payoff for the bug hunter", mean_payoff_bug_hunter)
print("initial cost of patch for the defender", mean_payoff_defender)

###############################################################################DATA ANALYSIS OF THE GAME########################################################################################################
#Set the parameters for the test
mean_bug_hunter = mean_payoff_bug_hunter 
mean_defender = mean_payoff_defender 
alpha = 0.05 
sample_bug_hunter = bug_hunter_array
sample_defender = defender_array

#Print sample of data from the population
print("Payoff sample for the bug hunter: \n",sample_bug_hunter)
print("Cost of patch sample for the defender: \n",sample_defender)

print("Average payoff for the bug hunter", mean_payoff_bug_hunter)
print("Cost of patch for the defender", mean_payoff_defender)

#Perform the z-test for the bug hunter
z_stat_bh, p_value_bh = ztest(sample_bug_hunter, value = mean_bug_hunter)

#Check the p_value for bug hunter
if p_value_bh < alpha:
    print("The hypothized value is different from the sampled mean for the average payoff of the bug hunter")
else:
    print("The hypothized value is equal to the sampled mean for the average payoff of the bug hunter")
    
#Perform the z-test for the defender
z_stat_def, p_value_def = ztest(sample_defender, value = mean_defender)
#Check the p_value for defender
if p_value_def < alpha:
    print("The hypothized value is equal to the sampled mean for the average cost of patch for the defender")
else:
    print("The hypothized value is equal to the sampled mean for the average cost of patch for the defender")

#Confidence interval at 95% for the bug hunter
sample_mean_bh = numpy.mean(sample_bug_hunter)
sample_std_bh = numpy.std(sample_bug_hunter)
z_critical_bh = stats.norm.ppf(q = 1-alpha/2)
margin_of_error_bh = z_critical_bh * (sample_std_bh / numpy.sqrt(len(sample_bug_hunter)))
confidence_interval_bh = (sample_mean_bh - margin_of_error_bh, sample_mean_bh + margin_of_error_bh)
print("Confidence interval at 95 percent for the average payoff for the bug hunter ",num_rounds,"rounds: ",confidence_interval_bh)

#Confidence interval at 95% for the defender
sample_mean_def = numpy.mean(sample_defender)
sample_std_def = numpy.std(sample_defender)
z_critical_def = stats.norm.ppf(q = 1-alpha/2)
margin_of_error_def = z_critical_def * (sample_std_def / numpy.sqrt(len(sample_defender)))
confidence_interval_def = (sample_mean_def - margin_of_error_def, sample_mean_def + margin_of_error_def)
print("Confidence interval at 95 percent for the average cost of patch in ",num_rounds,"rounds: ",confidence_interval_def)
