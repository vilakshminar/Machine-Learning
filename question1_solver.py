import math
from collections import defaultdict
import pdb

def tree(): return defaultdict(tree)

class Question1_Solver:
   	def __init__(self):
		self.id3_tree = self.learn('train.data');
        	return;

	def parse(self, data, attr, attr_hash, val1, val2):
        	y = []
        	n = []
        	q = []

        	for row in data:
			#print row
			instance1 = []
                	instance = row.split()
			instance[1] = instance[1].replace(',','')
			instance1.append(instance[0])
			for c in instance[1]:
				instance1.append(c)
			#print instance
                	if (instance1[attr_hash[attr]] == val1):
                        	y.append(row)
                	elif (instance1[attr_hash[attr]] == val2):
                        	n.append(row)
                	else:
                        	q.append(row)

        	return y, n, q

	def entropy(self, dataSet, attr, attr_hash, val1, val2):
        	data_y, data_n, data_q = self.parse(dataSet, attr, attr_hash, val1, val2);
        	len_dataSet = float(len(data_y) + len(data_n) + len(data_q))
		val_data = []
		val_data.append(float(len(data_y)))
		val_data.append(float(len(data_n)))
		val_data.append(float(len(data_q)))
        	entropy_val = 0.0
        	#print "Entropy"
        	#print
        	#print data_y
        	#print data_n
        	#print val_data, val_data.keys(), val_data.values(), len(dataSet)
        	for val in val_data:
                	if (val != 0):
				p = (val/len_dataSet)
                        	entropy_val += (-p) * math.log(p, 2)

        	return entropy_val


	def if_gain(self, data, attr, attr_hash):
        	en = 0.0

        	data_y, data_n, data_q = self.parse(data, attr, attr_hash, "y", "n")
		len_datay = float(len(data_y))
		len_datan = float(len(data_n))
		len_dataq = float(len(data_q))
        	#print val_data, val_data.keys(), val_data.values()

        	total_inst = len_datay + len_dataq + len_datan

        	for val in "ynq":
                	if (val == "y"):
                        	#print "y list"
                        	#print data_y
				prob = len_datay / total_inst
                        	en += prob * self.entropy(data_y, "men", attr_hash, "republican", "democrat")
                        	#print "entropy y =",entropy(data_y, "men", attr_hash, "republican", "democrat")
                	elif (val == "n"):
                        	#print "n list"
                        	#print data_n
				prob = len_datan / total_inst
                        	en += prob * self.entropy(data_n, "men", attr_hash, "republican", "democrat")
                        	#print "entropy n = ",entropy(data_n, "men", attr_hash, "republican", "democrat")
                	else:
                        	#print "? list"
                        	#print data_q
				prob = len_dataq / total_inst
                        	en += prob * self.entropy(data_q, "men", attr_hash, "republican", "democrat")
                	#for row in data:
                	#       instance = row.split()
                	#       if ((instance[1]+"y") == val):
                	#               data_attr_y.append(row)
                	#       else
                	#               data_attr_n.append(row) 
        	root_entropy = self.entropy(data, "men", attr_hash, "republican", "democrat")
        	#print "root_entropy =",root_entropy
        	ig = root_entropy - en
        	#print "ig =",ig
		return ig

	def bestattr(self, data, attr_list, attr_hash):
        	#print data
        	#print
        	#for row in data:
                #	instance = row.split()
#               	print instance[1]
        	#attr = "humidity"
		best_attr = ""
		best_attr_val = float("-inf")
		for attr in attr_list:
			if attr != "men":
				ig = self.if_gain(data, attr, attr_hash)
				if (ig > best_attr_val):
					best_attr = attr
					best_attr_val = ig
					

		#print attr_hash
		#print attr_list
		#print attr_list.index(max(attr_list)), "++ ", attr_hash[attr_list.index(max(attr_list))]
		#print "best attr = ",best_attr
		return best_attr

	def getsubDataSet(self, dataSet, attr_hash, attr, val):
		ret_list = []
		for row in dataSet:
			instance1 = []
			instance = row.split()
			instance[1] = instance[1].replace(',','')
			instance1.append(instance[0])
			for c in instance[1]:
				instance1.append(c)
			if(instance1[attr_hash[attr]] == val):
				ret_list.append(row)

		return ret_list
			
		
	def id3_decision_tree(self, dataSet, attr_list, attr_hash, attr):
			
		if not dataSet or ((len(attr_list)-1) <= 0):
			cols = []
			for line in dataSet:
				line = line.split()
				cols.append(line[0])
			count_rep = cols.count('republican')
			count_dem = cols.count('democrat')
			#print "count_rep = ", count_rep, "count_dem = ", count_dem
			return 'republican' if count_rep >= count_dem else 'democrat'
		else:
			cols = []
			for line in dataSet:
				line1 = []
				line = line.split()
				line[1] = line[1].replace(',','')
				line1.append(line[0])
				for c in line[1]:
					line1.append(c)
				cols.append(line1[attr_hash[attr]])

			if (cols.count(cols[0]) == len(cols)):
				#print "returning here"
				return cols[0]
			else:

				chosen_attr = self.bestattr(dataSet, attr_list, attr_hash)
				
				#dtree = {chosen_attr:{}}
				dtree = tree()
				#print "chosen_attr = ", chosen_attr
				chosen_attr_dataSet = []
				#best_y_dataSet = getsubDataSet(dataSet, best_attr, "y")
				#best_n_dataSet = getsubDataSet(dataSet, best_attr, "y")
				#best_q_dataSet = getsubDataSet(dataSet, best_attr, "y")
				# 0-y, 1-n, 2-q
				a_list = [ a for a in attr_list if chosen_attr != a ]
				#print "a_list = ", a_list
				chosen_attr_dataSet = self.getsubDataSet(dataSet, attr_hash, 
								chosen_attr, 'y')
				#print "sDataSet = ", chosen_attr_dataSet
				#a = raw_input()
				dtree[chosen_attr]['y'] = self.id3_decision_tree(chosen_attr_dataSet, 
							a_list, attr_hash, attr)	

				chosen_attr_dataSet = self.getsubDataSet(dataSet, attr_hash, 
								chosen_attr, 'n')
				dtree[chosen_attr]['n'] = self.id3_decision_tree(chosen_attr_dataSet, 
							a_list, attr_hash, attr)	

				chosen_attr_dataSet = self.getsubDataSet(dataSet, attr_hash, 
								chosen_attr, 'q')
				dtree[chosen_attr]['q'] = self.id3_decision_tree(chosen_attr_dataSet, 
							a_list, attr_hash, attr)

				#print "best attr = ", best_attr, "tree ", tree
				#aa = raw_input()

				return dtree	

			
	def get_attr_hash(self):
		attr_hash = {}			
		attr_hash["men"] = 0
		attr_hash["hand"] = 1
		attr_hash["water"] = 2
		attr_hash["adoption"] = 3
		attr_hash["physician"] = 4
		attr_hash["elsalv"] = 5
		attr_hash["religious"] = 6
		attr_hash["antisat"] = 7
		attr_hash["aid"] = 8
		attr_hash["missile"] = 9
		attr_hash["immigration"] = 10
		attr_hash["synfuel"] = 11
		attr_hash["education"] = 12
		attr_hash["superfund"] = 13
		attr_hash["crime"] = 14
		attr_hash["dutyfree"] = 15
		attr_hash["export"] = 16
		return attr_hash

    	# Add your code here.
   	# Read training data and build your decision tree
    	# Store the decision tree in this class
    	# This function runs only once when initializing
    	# Please read and only read train_data: 'train.data'
    	def learn(self, train_data):
		attr_hash = self.get_attr_hash()
		#print "attr_hash = ",attr_hash, "humid = ",attr_hash["humidity"]
		with open("train.data", "r") as f:
        		data = f.read().splitlines();

		id3_tree = self.id3_decision_tree(data, [a for a in attr_hash.keys() if a != "men"], attr_hash, "men") 
		#self.bestattr(data, attr_hash)
		#pdb.set_trace()

        	return id3_tree;

	def skim_id3(self, id3_tree, query_list, attr_hash):
		if isinstance(id3_tree, basestring):
			return id3_tree
		else:
			attr_list = id3_tree.keys()
			attr = attr_list[0]
			return self.skim_id3(id3_tree[attr][query_list[attr_hash[attr]-1]], query_list, attr_hash)

    	# Add your code here.
    	# Use the learned decision tree to predict
    	# query example: 'n,y,n,y,y,y,n,n,n,y,?,y,y,y,n,y'
    	# return 'republican' or 'republican'
    	def solve(self, query):
		query1 = []
		query = query.replace(',','')
		for c in query:
			query1.append(c)
		
		#print query1
		attr_hash = self.get_attr_hash()
		query2 = ['q' if x == '?' else x for x in query1]
		ans = self.skim_id3(self.id3_tree, query2, attr_hash)
		#pdb.set_trace()
		#return ans
		return ans 
        	#return 'democrat';

