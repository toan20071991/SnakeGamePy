import arcade
import threading
import random
import time

class Snake:
	def __init__(self, X, Y, size, step, width, height, level):
		self.posX = X
		self.posY = Y
		self.size = size
		self.step = step
		self.direction = "w"
		self.body = [(X - size, Y), (X - 2 * size, Y), (X - 3 * size, Y)]
		self.extendBody = []
		self.width = width
		self.height = height
		self.level = level
		random.seed(time.time())
		self.foodX = ((random.random() * self.width)//self.size)*self.size
		self.foodY = ((random.random() * self.height)//self.size)*self.size
		self.gameOver = False
		self.score = 0
	
	def createFood(self):
		self.foodX = ((random.random() * self.width)//self.size)*self.size
		self.foodY = ((random.random() * self.height)//self.size)*self.size
	
	def gameLogic(self):
		if (self.posX == self.foodX) & (self.posY == self.foodY):
			self.score += 1
			# store new body
			self.extendBody.insert(0,(self.foodX, self.foodY))
			# create new food
			self.createFood()
		
		# check if self touch boundery
		if (self.posX >= self.width) | (self.posY >= self.height) \
			| (self.posX <= 0) | (self.posY <= 0):
				self.gameOver = True
	
	def drawGame(self):
		self.startGame()
		while self.gameOver == False:
			arcade.start_render()
			# draw self head
			arcade.draw_rectangle_filled(self.posX, self.posY,\
				 self.size, self.size, arcade.color.RED)
			# draw self body
			for pos in self.body:
				arcade.draw_rectangle_filled(pos[0], pos[1],\
					 self.size, self.size, arcade.color.BLUE)
			# draw food
			arcade.draw_rectangle_filled(self.foodX, self.foodY,\
				 self.size, self.size, arcade.color.GREEN)
			# draw score
			arcade.draw_text(str(self.score), 20, self.height -20, (0,0,0), 15)
			arcade.finish_render()
			
			self.gameLogic()
			self.move()
			time.sleep(1/self.level)

	def startGame(self):
		arcade.open_window(self.width, self.height, "DEMO")
		arcade.set_background_color(arcade.color.WHITE)
	def move(self):
		#update body
		self.body.insert(0, (self.posX, self.posY))
		if (len(self.extendBody) != 0):
			if (self.extendBody[-1] == self.body[-1]):
				self.extendBody.pop()
			else:
				self.body.pop()
		else:
			self.body.pop()
		#update head
		if self.direction == "w":
			self.posY += self.step
		elif self.direction == "a":
			self.posX -= self.step
		elif self.direction == "d":
			self.posX += self.step
		elif self.direction == "s":
			self.posY -= self.step

	def getInput(self):
		while self.gameOver == False:
			cmd = input()
			if (cmd == "w") | (cmd == "s") | (cmd == "a") | (cmd == "d"):
				self.direction = cmd

def main():
	#create snake
	basicSnake = Snake((250//20)*20, (250//20)*20, 20, 20, 500, 500, 10)

	try:
		#create thread to read input
		task1 = threading.Thread(target=basicSnake.getInput)
		#run game
		task2 = threading.Thread(target=basicSnake.drawGame)
		task1.start()
		task2.start()
	except:
		print("Error create thread")

if __name__ == "__main__":
	main()
