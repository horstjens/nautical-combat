import random

def generate(maxx = 20, maxy = 20):
	"""Generate random tile map max differents between tiles = 1
	Legend:
	3... Deep water
	4... Normal Water
	5... Shallow waer
	6... Beach
	7... Land
	8... Highland"""
	
	watermap = []
	seed = [3,3,4,4,4,4,5,5,6,6,7,8]
	log = {3:0, 4:0, 5:0 , 6:0, 7:0, 8:0}
	
	x = 0
	y = 0
	#x = maxx // 2
	#y = maxy // 2
	
	for line in range(maxy):
		watermap.append("")
		for char in range(maxx):
			tile = random.choice(seed)
			maxneighbour = None
			minneighbour = None
			for dx in [-1,0,1]:
				for dy in [-1,0,1]:
					if dx == 0 and dy == 0:
						continue
					try:
						neighbour = int(watermap[line + dy][char + dx])
					except:
						neighbour = None
						continue
					if maxneighbour is None:
						maxneighbour = neighbour
					if minneighbour is None:
						minneighbour = neighbour
					if maxneighbour > tile:
						tile = maxneighbour - 1
					elif maxneighbour < tile:
						tile = maxneighbour + 1
					if minneighbour < tile:
						tile = minneighbour + 1
					elif minneighbour > tile:
						tile = minneighbour - 1
			watermap[line] += str(tile)
	mapfile = open("level1.txt","w")
	with mapfile:
		for line in watermap:
			mapfile.write(line + "\n")
	print("----- Fertig! -----")
	
if __name__ == "__main__":
	generate()
