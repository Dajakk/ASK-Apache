"""
Alamakota
"""
import re

class Node( object ):
	"""
	Alamakota
	"""

	def toString(self):
		"""
		Alamakota
		"""
		print "::NODE::"
		print self.name
		print self.rootData

		for dat in self.data:
			dat.toString( )

	def __str__(self):
		temp = "<fieldset>"
		#temp = temp + "::NODE::" + "<br />"
		#temp = temp + self.name + "<br />"
		temp += "<legend>%s</legend>" % self.rootData

		for dat in self.data:
			temp += "%s<br />" % dat

		temp += "</fieldset>"
		return temp

	def __init__(self, name, rootData, nodes, data):
		"""
		Alamakota
		"""
		self.name = name
		self.rootData = rootData
		self.nodes = nodes
		self.data = data

class Data( object ):
	"""
	Alamakota
	"""

	def __init__(self, comments, key, value):
		"""
		Alamakota
		"""
		self.comments = comments
		self.key = key
		self.value = value

	def toString(self):
		"""
		Alamakota
		"""
		print "::DATA::"
		print self.comments
		print self.key
		print self.value

	def __str__(self):
		temp = ""
		#temp = temp + "::DATA::" + "<br />"
		#temp = temp + self.comments.__str__() + "<br />"
		temp += "<label>%s</label>" % self.key
		temp += "<input value=\"%s\"></input><br />" % self.value
		return temp


class HttpConf( object ):
	"""
	Alamakota
	"""
	comment = re.compile( r"#.*" )
	dataline = re.compile( r"[A-Za-z].*" )
	newNodeStart = re.compile( r"[<][A-Za-z].*" )
	newNodeEnd = re.compile( r"</.*" )

	def __init__(self):
		self.global_root_name = ""
		self.global_root_data = []
		self.opening_line = ""
		self.name = ""
		self.rootData = ""
		self.nodes = []
		self.data = []


	def save_to_file(self, filename):
		"""
		Alamakota
		"""
		file = open( filename, 'w' )

		for d in self.data:
			d.toString( )

			file.write( "\n" )
			#write all comments
			for comment in d.comments:
				file.write( comment + "\n" )

			values = ""
			for v in d.value:
				values = values + " " + v

			file.write( d.key + " " + values + "\n" )

		file.write( "\n" )

		for node in self.nodes:
			file.write( "\n" )

			node_root_values = ""

			for s in node.rootData:
				node_root_values = node_root_values + " " + s

			file.write( "<" + node.name + " " + node_root_values + ">" + "\n" )


			#write content
			for node_data in node.data:
				node_data_value = ""
				for s in node_data.value:
					node_data_value = node_data_value + " " + s

				file.write( "\t" + node_data.key + " " + node_data_value + " \n" )

			file.write( "</" + node.name + ">" + "\n" )
		#write virtual host ending
		file.write( "</VirtualHost>" )

		file.close( )

	def parse(self, filename):
		"""
		Alamakota
		"""
		file = open( filename, 'r' )

		input_file = []
		for line in file:
			input_file.append( line.strip( ) )

		file.close( )
		comments = []

		i = 0

		while i < len( input_file ):
			line = input_file[i].strip( )

			if self.comment.match( line ):
				comments.append( line )

			elif self.dataline.match( line ):
				#print line
				key = line.split( " " )[0]
				value = line.split( " " )[1:]
				self.data.append( Data( comments, key, value ) )
				comments = []

			elif self.newNodeStart.match( line ):
				line = line.replace( "<", "" )
				line = line.replace( ">", "" )

				name = line.split( " " )[0]
				data = line.split( " " )[1:]
				currentNodeData = []

				print name
				print data

				i += 1
				line = input_file[i]
				while not self.newNodeEnd.match( line ):
					print line

					if self.dataline.match( line ):
						#print line
						key = line.split( " " )[0]
						value = line.split( " " )[1:]
						currentNodeData.append( Data( comments, key, value ) )
						comments = []

					i += 1
					line = input_file[i]
				currentNode = Node( name, data, [], currentNodeData )
				self.nodes.append( currentNode )

			i += 1


class VirtualHost( object ):
	"""
	Alamakota
	"""
	comment = re.compile( r"#.*" )
	dataline = re.compile( r"[A-Za-z].*" )
	newNodeStart = re.compile( r"[<][A-Za-z].*" )
	newNodeEnd = re.compile( r"</.*" )

	def __init__(self):
		self.global_root_name = ""
		self.global_root_data = []
		self.opening_line = ""

		self.name = ""
		self.rootData = ""
		self.nodes = []
		self.data = []

	def save_to_file(self, filename):
		"""
		Alamakota
		"""
		file = open( filename, 'w' )

		#write virtual host header
		r_data = ""
		for s in self.global_root_data:
			r_data = r_data + " " + s
		file.write( "<" + self.global_root_name + " " + r_data + ">" + "\n" )

		for d in self.data:
			d.toString( )

			file.write( "\n" )
			#write all comments
			for comment in d.comments:
				file.write( comment + "\n" )

			values = ""
			for v in d.value:
				values = values + " " + v

			file.write( d.key + " " + values + "\n" )

		file.write( "\n" )

		for node in self.nodes:
			file.write( "\n" )

			node_root_values = ""

			for s in node.rootData:
				node_root_values = node_root_values + " " + s

			file.write( "<" + node.name + " " + node_root_values + ">" + "\n" )


			#write content
			for node_data in node.data:
				node_data_value = ""
				for s in node_data.value:
					node_data_value = node_data_value + " " + s

				file.write( "\t" + node_data.key + " " + node_data_value + " \n" )

			file.write( "</" + node.name + ">" + "\n" )
		#write virtual host ending
		file.write( "</VirtualHost>" )

		file.close( )

	def parse(self, filename):
		"""
		Alamakota
		"""
		file = open( filename, 'r' )

		input_file = []
		for line in file:
			input_file.append( line.strip( ) )

		file.close( )
		comments = []

		i = 0

		#parsing <VirtualHost ...>
		while not self.newNodeEnd.match( line ):
			i += 1

		line = input_file[i]

		# now we have the beginning line
		line = line.replace( "<", "" )
		line = line.replace( ">", "" )

		self.global_root_name = line.split( " " )[0]
		self.global_root_data = line.split( " " )[1:]

		i += 1

		while i < len( input_file ):
			line = input_file[i].strip( )

			if self.comment.match( line ):
				comments.append( line )

			elif self.dataline.match( line ):
				#print line
				key = line.split( " " )[0]
				value = line.split( " " )[1:]
				self.data.append( Data( comments, key, value ) )
				comments = []

			elif self.newNodeStart.match( line ):
				line = line.replace( "<", "" )
				line = line.replace( ">", "" )

				name = line.split( " " )[0]
				data = line.split( " " )[1:]
				currentNodeData = []

				print name
				print data

				i += 1
				line = input_file[i]
				while not self.newNodeEnd.match( line ):
					print line

					if self.dataline.match( line ):
						#print line
						key = line.split( " " )[0]
						value = line.split( " " )[1:]
						currentNodeData.append( Data( comments, key, value ) )
						comments = []

					i += 1
					line = input_file[i]
				currentNode = Node( name, data, [], currentNodeData )
				self.nodes.append( currentNode )

			i += 1


if __name__ == "__main__":
	virtualHost = VirtualHost( )
	virtualHost.parse( "default" )

	data = virtualHost.data

	nodes = virtualHost.nodes


	#print "-----------------_NODES_----------------"

	#for node in nodes:
	#    node.toString()


	virtualHost.save_to_file( "saved_file" )
	print "file saved"

	httpConf = HttpConf( )
	httpConf.parse( "apache2.conf" )
	httpConf.save_to_file( "ap2.conf" )

	#print len(data)
	#print data
	#for dat in data:
	#    dat.toString()
