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
    expectedTotalReward = calculateExpectedTotalRewards(totalAmountStaked, totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset)
    gainAsFraction = expectedTotalReward/newAmountStaked # needs to be multiplied by 100 to get the % value
    durationAsFractionOfYear = lockingDuration/365       # needs to be multiplied by 100 to get the % value
    return gainAsFraction / durationAsFractionOfYear


# Estimated total rewards, non paused positions. 
def calculateExpectedTotalRewards(totalAmountStaked, totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset):
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



# sample values
totalAmountStaked = 282000000000000000000 / 10** 18 # * 10 ** 6   # get from the contract
dailyRewards = 8000000 / 365    # get from the contract
offset = 150                    # get from the contract
totalWeight = 246335000000000000000000 / 10**18 #* 10 ** 6       # get from the contract

print("Current Avg APR: {}% (based on current staking participation and average locking duration of {} days)".format(calculateCurrentAverageAPR(totalAmountStaked, totalWeight, dailyRewards)*100, getAverageLockingDuration(totalAmountStaked, totalWeight, offset)))

#sample values for new staking position
newAmountStaked = 10 ** 6
lockingDuration = 728
print()
print("New locking position with amount = {} and duration = {}:".format(newAmountStaked,lockingDuration))
print("Expected APR:{}%".format(100*calculateMyExpectedAPRForNewPosition(totalAmountStaked, totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset)) )
print("Expected Total Rewards:", calculateExpectedTotalRewards(totalAmountStaked, totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset))