class Question3_Solver:
	def __init__(self):
		self.centroid = [(30,60), (150,60), (90,130)]
		return
	
	# Add your code here.
	# Return the centroids of clusters.
	# You must use [(30, 30), (150, 30), (90, 130)] as initial centroids
	
	def get_cluster(self, points, centroids):
		distance, cluster = [], []
		for point in points:
			distance.append(((centroids[0][0] - point[0])**2 + (centroids[0][1] - point[1])**2) ** 0.5)
			distance.append(((centroids[1][0] - point[0])**2 + (centroids[1][1] - point[1])**2) ** 0.5)
			distance.append(((centroids[2][0] - point[0])**2 + (centroids[2][1] - point[1])**2) ** 0.5)
			cluster.append(distance.index(min(distance)))
			distance = []
		return cluster

	def get_means(self, cluster, points):
		cluster_dict_x = [[],[],[]]
		cluster_dict_y = [[],[],[]]
		for i in range(len(cluster)):
			cluster_dict_x[cluster[i]].append(points[i][0])
			cluster_dict_y[cluster[i]].append(points[i][1])
		self.centroid = []
		for val in range(3):
			self.centroid.append((float(sum(cluster_dict_x[val]))/float(len(cluster_dict_x[val])), float(sum(cluster_dict_y[val]))/float(len(cluster_dict_y[val]))))
		return points

	def solve(self, points):
		center = self.centroid	
		same = False
		while True:
			cluster = self.get_cluster(points, self.centroid)
			means = self.get_means(cluster, points)
			if center[0][0] == self.centroid[0][0] and center[0][1] == self.centroid[0][1]:
				same = True
			else:
				same = False
			if center[1][0] == self.centroid[1][0] and center[1][1] == self.centroid[1][1]:
				same = True
			else:
				same = False
			if center[2][0] == self.centroid[2][0] and center[2][1] == self.centroid[2][1]:
				same = True
			else:
				same = False
			if same:
				break
			center = self.centroid
		#return [(48,47),(128,80),(48,103)]
		return self.centroid 
