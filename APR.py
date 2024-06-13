# This function returns the current average locking duration of 1 staked LSK. 
# To get the expected APR, one needs to stake for the duration returned by this function
def getAverageLockingDuration(totalAmountStaked, totalWeight, offset):
    return (totalWeight - offset * totalAmountStaked)/totalAmountStaked 



# This function calculates the current expected average APR 
# Should be shown after multiplied by 100%
def calculateCurrentAverageAPR(totalAmountStaked, totalWeight, dailyRewards):
    averageLockingDuration = getAverageLockingDuration(totalAmountStaked, totalWeight, offset)
    expectedTotalRewardPerLSK = ( offset + (averageLockingDuration +1) / 2) * averageLockingDuration * dailyRewards/totalWeight
    durationAsFractionOfYear = averageLockingDuration/365       
    return expectedTotalRewardPerLSK / durationAsFractionOfYear


# Expected APR for a new position
def calculateMyExpectedAPRForNewPosition(totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset):
    expectedTotalReward = calculateExpectedTotalRewards(totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset)
    gainAsFraction = expectedTotalReward/newAmountStaked # needs to be multiplied by 100 to get the % value
    durationAsFractionOfYear = lockingDuration/365       # needs to be multiplied by 100 to get the % value
    return gainAsFraction / durationAsFractionOfYear


# Estimated total rewards, non paused positions. 
def calculateExpectedTotalRewards(totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset):
    totalWeight += newAmountStaked * (lockingDuration + offset) 
    expectedTotalReward = 0
    for i in range(lockingDuration):
        remainingDaysToConsider = lockingDuration - i
        weight = newAmountStaked *(remainingDaysToConsider + offset)
        expectedTotalReward += (weight * dailyRewards)/totalWeight
        totalWeight -= newAmountStaked
    return expectedTotalReward



# sample values
totalAmountStaked = 500 # * 10 ** 6   # get from the contract
dailyRewards = 8000000 / 365    # get from the contract
offset = 150                    # get from the contract
totalWeight = 295000 #* 10 ** 6       # get from the contract

dailyRewards = min(totalAmountStaked/365, dailyRewards)
print("Current Avg APR: {}% (based on current staking participation and average locking duration of {} days)".format(calculateCurrentAverageAPR(totalAmountStaked, totalWeight, dailyRewards)*100, getAverageLockingDuration(totalAmountStaked, totalWeight, offset)))

#sample values for new staking position
newAmountStaked = 100 
lockingDuration = 440
print()
print("New locking position with amount = {} and duration = {}:".format(newAmountStaked,lockingDuration))
print("Expected APR:{}%".format(100*calculateMyExpectedAPRForNewPosition(totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset)) )
print("Expected Total Rewards:", calculateExpectedTotalRewards(totalWeight, dailyRewards, newAmountStaked, lockingDuration, offset))