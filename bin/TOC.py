from fpdf import FPDF

def str_repeat(s,t): return s*int(t)

class TOC(FPDF):
	def __init__(this, orientation='P',unit='mm',format='A4'):
		this._toc=[]
		this._numbering=0
		this._numberingFooter=0
		this._numPageNum=1
		this.in_toc = 0
		FPDF.__init__(this,orientation,unit,format)

	def add_page(this,orientation=''):
		FPDF.add_page(this,orientation)
		if(this._numbering):
			this._numPageNum+=1

	def start_page_nums(this):
		this._numbering=1
		this._numberingFooter=1

	def stop_page_nums(this):
		this._numbering=0

	def num_page_no(this):
		return this._numPageNum

	def toc_entry(this,txt,level=0):
		this._toc+=[{'t':txt,'l':level,'p':this.num_page_no()}]

	def insert_toc(this,location=1,labelSize=20,entrySize=10,tocfont='Times',label='Table of Contents'):
		#make toc at end
		this.in_toc = 1
		this.stop_page_nums()
		this.add_page()
		tocstart=this.page

		this.set_font(tocfont,'B',labelSize)
		this.cell(0,5,label,0,1,'C')
		this.ln(10)

		for t in this._toc:
			# Create an in-document link
			tocLink = this.add_link()
			this.set_link(tocLink, 0, t['p'] + 1)

			#Offset
			level=t['l']
			if(level>0):
				this.cell(level*8, this.font_size+2)
			weight=''
			if(level==0):
				weight='B'
			Str=t['t']
			this.set_font(tocfont,weight,entrySize)
			strsize=this.get_string_width(Str)
			this.cell(strsize+2,this.font_size+2,Str, 0, 0, '', False, tocLink)

			#Filling dots
			this.set_font(tocfont,'',entrySize)
			PageCellSize=this.get_string_width(str(t['p']))+2
			w=this.w-this.l_margin-this.r_margin-PageCellSize-(level*8)-(strsize+2)
			nb=w/this.get_string_width('.')
			dots=str_repeat('.',nb)
			this.cell(w,this.font_size+2,dots,0,0,'R')

			#Page number
			this.cell(PageCellSize,this.font_size+2,str(t['p']),0,1,'R', False, tocLink)

		#grab it and move to selected location
		n=this.page
		n_toc = n - tocstart + 1
		last = []
		lastlinks = []

		# Store TOC pages and page links
		for i in xrange(tocstart,n+1):
			# Store page
			last+=[this.pages[i]]
			# Store links
			lastlinks+=[this.page_links[i]]

		# Move remaining pages and page links
		for i in xrange(tocstart-1,location-1,-1):
			# Move page
			this.pages[i+n_toc]=this.pages[i]
			# Move links
			this.page_links[i+n_toc]=this.page_links[i]

		# Put TOC pages and page links at insert point
		for i in xrange(0,n_toc):
			this.pages[location + i]=last[i]
			this.page_links[location + i]=lastlinks[i]

		# Renumber page refererences in all internal links
		for i in this.links:
			this.links[i] = [this.links[i][0] + n_toc, this.links[i][1]]

		this.in_toc = 0