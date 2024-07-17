# This function returns the current average locking duration of 1 staked LSK. 
# To get the expected APR, one needs to stake for the duration returned by this function
def getAverageLockingDuration(totalAmountStaked, totalWeight, offset):
    return (totalWeight - offset * totalAmountStaked)/totalAmountStaked 



# This function calculates the current expected average APR 
# Should be shown after multiplied by 100%
def calculateCurrentAverageAPR(totalAmountStaked, totalWeight, dailyRewards):
    dailyRewards = min(totalAmountStaked/365, dailyRewards)
    print("Current daily rewards:", dailyRewards)
    averageLockingDuration = getAverageLockingDuration(totalAmountStaked, totalWeight, offset)
    expectedTotalRewardPerLSK = ( offset + (averageLockingDuration +1) / 2) * averageLockingDuration * dailyRewards/totalWeight
    durationAsFractionOfYear = averageLockingDuration/365       
    return expectedTotalRewardPerLSK / durationAsFractionOfYear


# Expected APR for a new position
def calculateMyExpectedAPRForNewPosition(totalAmountStaked, totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset):
    expectedTotalReward = calculateExpectedTotalRewardsNewPosition(totalAmountStaked, totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset)
    gainAsFraction = expectedTotalReward/newAmountStaked # needs to be multiplied by 100 to get the % value
    durationAsFractionOfYear = lockingDuration/365       # needs to be multiplied by 100 to get the % value
    return gainAsFraction / durationAsFractionOfYear

# Expected APR for current position   
def calculateExpectedAPRCurrentPosition(totalAmountStaked, totalWeight, dailyRewards, amountStaked, remainingLockingDuration, offset):
    # apply capping if necessary
    dailyRewards = min(totalAmountStaked/365, dailyRewards)
    expectedTotalReward = calculateExpectedTotalRewards(totalAmountStaked, totalWeight, dailyRewards, amountStaked, remainingLockingDuration, offset)
    gainAsFraction = expectedTotalReward/amountStaked # needs to be multiplied by 100 to get the % value
    durationAsFractionOfYear = remainingLockingDuration/365       # needs to be multiplied by 100 to get the % value
    return gainAsFraction / durationAsFractionOfYear
   

# Estimated total rewards, for existing non-paused position. 
def calculateExpectedTotalRewards(totalAmountStaked, totalWeight, dailyRewards, amountStaked, remainingLockingDuration, offset):
    expectedTotalReward = 0
    for i in range(lockingDuration):
        remainingDaysToConsider = lockingDuration - i
        weight = amountStaked *(remainingDaysToConsider + offset)
        expectedTotalReward += (weight * dailyRewards)/totalWeight
        totalWeight -= amountStaked
    return expectedTotalReward



# Estimated total rewards, new position to be added. 
def calculateExpectedTotalRewardsNewPosition(totalAmountStaked, totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset):
    dailyRewards = min((totalAmountStaked+newAmountStaked)/365, dailyRewards)
    print("Daily Rewards after new vote:", dailyRewards)
    totalWeight += newAmountStaked * (lockingDuration + offset) 
    expectedTotalReward = 0
    for i in range(lockingDuration):
        remainingDaysToConsider = lockingDuration - i
        weight = newAmountStaked *(remainingDaysToConsider + offset)
        expectedTotalReward += (weight * dailyRewards)/totalWeight
        totalWeight -= newAmountStaked
    return expectedTotalReward


# This function calculates the current expected average APR for paused positions
# Should be shown after multiplied by 100%
def calculateExpectedAverageAPRForPaused(totalAmountStaked, dailyRewards):
    # apply capping if necessary
    dailyRewards = min(totalAmountStaked/365, dailyRewards)
    return (dailyRewards*365)/ totalAmountStaked

# This function calculates the expected APR for an active position which is paused (v1)
def calculateMyAPRPaused1(pausedDuration,totalAmountStaked, totalWeight, dailyRewards, offset):
    # apply capping if necessary
    dailyRewards = min(totalAmountStaked/365, dailyRewards)
    avgLockingDuration = getAverageLockingDuration(totalAmountStaked, totalWeight, offset) 
    avgAPR = calculateExpectedAverageAPRForPaused(totalAmountStaked, dailyRewards)
    return (pausedDuration+offset)/(avgLockingDuration + offset) * avgAPR
    

## This function calculates the expected APR for an active position which is paused (v2)
def calculateMyAPRPaused2(stakedAmount, pausedDuration, totalWeight, dailyRewards, offset):
    # apply capping if necessary
    dailyRewards = min(totalAmountStaked/365, dailyRewards)
    yearlyRewards = dailyRewards * 365
    myWeight = stakedAmount * (pausedDuration + offset)
    expectedYearlyReward = myWeight * yearlyRewards/totalWeight
    expectedAPR = expectedYearlyReward / stakedAmount
    return expectedAPR
    

# sample values
totalAmountStaked = 24798713410444989982200000 #  # get from the contract
dailyRewards = 8000000 * 10**18 / 365    # get from the contract
offset = 150                    # get from the contract
totalWeight = 12339927205798896461149900000      # get from the contract

print("Current Avg APR: {}% (based on current staking participation and average locking duration of {} days)".format(calculateCurrentAverageAPR(totalAmountStaked, totalWeight, dailyRewards)*100, getAverageLockingDuration(totalAmountStaked, totalWeight, offset)))

#sample values for new staking position
newAmountStaked = 10 ** 6
lockingDuration = 347
print()
print("New locking position with amount = {} and duration = {}:".format(newAmountStaked,lockingDuration))
print("Expected APR:{}%".format(100*calculateMyExpectedAPRForNewPosition(totalAmountStaked, totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset)) )
print("Expected Total Rewards:", calculateExpectedTotalRewards(totalAmountStaked, totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset))
print()

print("======================================================")
print()
print("Current Avg APR for paused positions: {}% (based on current staking participation and average locking duration of {} days)".format(calculateExpectedAverageAPRForPaused(totalAmountStaked, dailyRewards)*100, getAverageLockingDuration(totalAmountStaked, totalWeight, offset)))

amountStaked = 100 * 10**18   # edit, pick any value
lockingDuration = 300         # edit, pick any value 
print()
print("Active (non-paused) position with amount={} LSK and duration={}. Current expected APR is:{}%".format(amountStaked/10**18, lockingDuration,calculateExpectedAPRCurrentPosition(totalAmountStaked, totalWeight, dailyRewards, amountStaked, lockingDuration, offset)*100))
print("Expected APR is position gets paused (v1 calculation): {}%".format(calculateMyAPRPaused1(lockingDuration,totalAmountStaked, totalWeight, dailyRewards, offset)*100))
print("Expected APR is position gets paused (v2 calculation): {}%".format(calculateMyAPRPaused2(newAmountStaked, lockingDuration, totalWeight, dailyRewards, offset)*100))
