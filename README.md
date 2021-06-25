Ship of Fools is a simple classic dice game. It is played with five standard 6-faced dice by two or more players. The game goal is to gather a 6, a 5 end a 4 (ship, captain and crew) in the mentioned order. The sum of the two remaining dice (cargo) is preferred as high as possible. The player with the highest cargo score wins the round.

Example: Each player gets to roll dices three times. If a player in the first round turn roll 6 4 3 3 1 the player can bank the 6 (ship), but the rest needs to be re-rolled since there is no 5. I the second round turn, if the player rolls 6 5 4 4 (four dice, since the 6 from last turn is banked) the player can bank the 5 (captain) and the 4 (crew). Now, the player has three choices of what to do with the remaining 6 and 4. The player can bank both and score 10 points or re-roll one or two of the dice and hope for a higher score. If the player in the second round turn instead  rolled 4 4 3 1 all dice needs to be re-rolled since there is no 5.

The division of responsibility between the different classes is as follows.

Die: Responsible for handling randomly generated integer values between 1 and 6.

DiceCup: Handles five objects (dice) of class Die. Has the ability to bank and release dice individually.  Can also roll dice that are not banked.

ShipOfFoolsGame: Responsible for the game logic and has the ability to play a round of the game resulting in a score. Also has a property that tells what accumulated score results in a winning state, for example 21.

Player: Responsible for the score of the individual player. Has the ability, given a game logic, play a round of a game. The gained score is accumulated in the attribute score.

PlayRoom: Responsible for handling a number of players and a game. Every round the room lets each player play, and afterwards check if any player have reached the winning score.
