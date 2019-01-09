from fpdf import FPDF

def str_repeat(s,t): return s*int(t)

class TOC(FPDF):
	def __init__(self, orientation='P',unit='mm',format='A4'):
		self._toc=[]
		self._numbering=0
		self._numberingFooter=0
		self._numPageNum=1
		self.in_toc = 0
		FPDF.__init__(self,orientation,unit,format)

	def add_page(self,orientation=''):
		FPDF.add_page(self,orientation)
		if(self._numbering):
			self._numPageNum+=1

	def start_page_nums(self):
		self._numbering=1
		self._numberingFooter=1

	def stop_page_nums(self):
		self._numbering=0

	def num_page_no(self):
		return self._numPageNum

	def toc_entry(self,txt,level=0):
		self._toc+=[{'t':txt,'l':level,'p':self.num_page_no()}]

	def insert_toc(self,location=1,labelSize=20,entrySize=10,tocfont='Times',label='Table of Contents'):
		#make toc at end
		self.in_toc = 1
		self.stop_page_nums()
		self.add_page()
		tocstart=self.page

		self.set_font(tocfont,'B',labelSize)
		self.cell(0,5,label,0,1,'C')
		self.ln(10)

		for t in self._toc:
			# Create an in-document link
			tocLink = self.add_link()
			self.set_link(tocLink, 0, t['p'] + 1)

			#Offset
			level=t['l']
			if(level>0):
				self.cell(level*8, self.font_size+2)
			weight=''
			if(level==0):
				weight='B'
			Str=t['t']
			self.set_font(tocfont,weight,entrySize)
			strsize=self.get_string_width(Str)
			self.cell(strsize+2,self.font_size+2,Str, 0, 0, '', False, tocLink)

			#Filling dots
			self.set_font(tocfont,'',entrySize)
			PageCellSize=self.get_string_width(str(t['p']))+2
			w=self.w-self.l_margin-self.r_margin-PageCellSize-(level*8)-(strsize+2)
			nb=w/self.get_string_width('.')
			dots=str_repeat('.',nb)
			self.cell(w,self.font_size+2,dots,0,0,'R')

			#Page number
			self.cell(PageCellSize,self.font_size+2,str(t['p']),0,1,'R', False, tocLink)

		#grab it and move to selected location
		n=self.page
		n_toc = n - tocstart + 1
		last = []
		lastlinks = []

		# Store TOC pages and page links
		for i in range(tocstart,n+1):
			# Store page
			last+=[self.pages[i]]
			# Store links
			lastlinks+=[self.page_links[i]]

		# Move remaining pages and page links
		for i in range(tocstart-1,location-1,-1):
			# Move page
			self.pages[i+n_toc]=self.pages[i]
			# Move links
			self.page_links[i+n_toc]=self.page_links[i]

		# Put TOC pages and page links at insert point
		for i in range(0,n_toc):
			self.pages[location + i]=last[i]
			self.page_links[location + i]=lastlinks[i]

		# Renumber page refererences in all internal links
		for i in self.links:
			self.links[i] = [self.links[i][0] + n_toc, self.links[i][1]]

		self.in_toc = 0