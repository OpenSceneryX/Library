#tag WindowBegin Window wndAbout   BackColor       =   &hFFFFFF   Backdrop        =   ""   CloseButton     =   True   Composite       =   True   Frame           =   0   FullScreen      =   False   HasBackColor    =   False   Height          =   300   ImplicitInstance=   True   LiveResize      =   True   MacProcID       =   0   MaxHeight       =   32000   MaximizeButton  =   False   MaxWidth        =   32000   MenuBar         =   ""   MenuBarVisible  =   True   MinHeight       =   64   MinimizeButton  =   True   MinWidth        =   64   Placement       =   2   Resizeable      =   False   Title           =   "#kWindowTitle"   Visible         =   True   Width           =   276   Begin Canvas cnvOSXLogo      AcceptFocus     =   ""      AcceptTabs      =   ""      AutoDeactivate  =   True      Backdrop        =   200112520      DoubleBuffer    =   False      Enabled         =   True      EraseBackground =   True      Height          =   52      HelpTag         =   ""      Index           =   -2147483648      InitialParent   =   ""      Left            =   20      LockBottom      =   ""      LockedInPosition=   False      LockLeft        =   ""      LockRight       =   ""      LockTop         =   ""      Scope           =   0      TabIndex        =   0      TabPanelIndex   =   0      TabStop         =   True      Top             =   14      UseFocusRing    =   True      Visible         =   True      Width           =   236   End   Begin StaticText txtWebAddress      AutoDeactivate  =   True      Bold            =   ""      DataField       =   ""      DataSource      =   ""      Enabled         =   True      Height          =   20      HelpTag         =   ""      Index           =   -2147483648      InitialParent   =   ""      Italic          =   ""      Left            =   20      LockBottom      =   ""      LockedInPosition=   False      LockLeft        =   ""      LockRight       =   ""      LockTop         =   ""      Multiline       =   False      Scope           =   0      TabIndex        =   1      TabPanelIndex   =   0      Text            =   "www.opensceneryx.com"      TextAlign       =   1      TextColor       =   "&c0000ff"      TextFont        =   "System"      TextSize        =   0      TextUnit        =   0      Top             =   80      Underline       =   ""      Visible         =   True      Width           =   236   End   Begin Timer Timer1      Height          =   32      Index           =   -2147483648      InitialParent   =   ""      Left            =   366      LockedInPosition=   False      Mode            =   2      Period          =   50      Scope           =   0      TabPanelIndex   =   0      Top             =   2      Width           =   32   End   Begin Canvas cnvAboutText      AcceptFocus     =   ""      AcceptTabs      =   ""      AutoDeactivate  =   True      Backdrop        =   ""      DoubleBuffer    =   False      Enabled         =   True      EraseBackground =   True      Height          =   168      HelpTag         =   ""      Index           =   -2147483648      InitialParent   =   ""      Left            =   20      LockBottom      =   ""      LockedInPosition=   False      LockLeft        =   ""      LockRight       =   ""      LockTop         =   ""      Scope           =   0      TabIndex        =   3      TabPanelIndex   =   0      TabStop         =   True      Top             =   112      UseFocusRing    =   True      Visible         =   True      Width           =   236   EndEnd#tag EndWindow#tag WindowCode	#tag Event		Sub Open()		  yScroll = cnvAboutText.height + 20		End Sub	#tag EndEvent	#tag MenuHandler		Function FileClose() As Boolean Handles FileClose.Action			me.close			Return True					End Function	#tag EndMenuHandler	#tag Property, Flags = &h0		yScroll As Integer = 0	#tag EndProperty	#tag Constant, Name = kAboutBoxContents, Type = String, Dynamic = True, Default = \"OpenSceneryX Installer Copyright \xC2\xA92010 Austin Goudge (austin@opensceneryx.com)\r\rMany thanks go to:\r\rSergio Santagada for allowing the icon to be based on his X-Plane\xC2\xAE icon artwork\r\rTom Kyler and Jordi Sayol for testing the Linux builds\r\rFabian for the Spanish translation\r\rOlivier Faivre for the French translation\r\rNicola Altafini for the Italian translation\r\rJordi Sayol for the Catalan translation\r\rDavid Gluck for the German translation\r\rAll the contributors to OpenSceneryX\x2C without which the installer would be kind of pointless!\r\r\r\rThis software uses Thomas Tempelmann\'s Zip Package (www.tempel.org) and Kevin Ballard\'s XMLDictionary module (www.tildesoft.com)", Scope = Public		#Tag Instance, Platform = Any, Language = it, Definition  = \"Copyright dell\'Installatore di OpenSceneryX  \r\r\xC2\xA92010 Austin Goudge (austin@opensceneryx.com)\r\rUn grazie infinito a:\r\rSergio Santagada per aver permesso di basare l\'icona sulla grafica di quella di X-Plane\xC2\xAE\r\rTom Kyler and Jordi Sayol per aver testato la versione Linux\r\rFabian per la traduzione in Spagnolo\r\rOlivier Faivre per la traduzione in Francese\r\rNicola Altafini per la traduzione in Italiano\r\rJordi Sayol per la traduzzione in Catalano\r\rDavid Gluck per la traduzione in Germano\r\rTutti quelli che hanno contribuito senza i quali l\'installatore non avrebbe potuto esserci.\r\rQuesto programma usa il pacchetto di Thomas Tempelmann (www.tempel.org) ed i moduli XMLDictionary di Kevin Ballard (www.tildesoft.com)"	#tag EndConstant	#tag Constant, Name = kWindowTitle, Type = String, Dynamic = True, Default = \"About OpenSceneryX Installer", Scope = Public	#tag EndConstant#tag EndWindowCode#tag Events txtWebAddress	#tag Event		Sub Open()		  me.mousecursor = system.cursors.FingerPointer		End Sub	#tag EndEvent	#tag Event		Function MouseDown(X As Integer, Y As Integer) As Boolean		  ShowURL("http://www.opensceneryx.com")		  		End Function	#tag EndEvent#tag EndEvents#tag Events Timer1	#tag Event		Sub Action()		  yScroll = yScroll - 1		  		  if yScroll <= -300 then		    yScroll = cnvAboutText.height + 20		  end if		  		  cnvAboutText.refresh		  		End Sub	#tag EndEvent#tag EndEvents#tag Events cnvAboutText	#tag Event		Sub Paint(g As Graphics)		  g.textSize = 9		  if Window(0) <> wndAbout then		    g.foreColor = &c888888		  end if		  g.drawString(kAboutBoxContents, 0, yScroll, me.width)		End Sub	#tag EndEvent#tag EndEvents