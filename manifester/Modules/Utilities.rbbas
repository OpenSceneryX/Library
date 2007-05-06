#tag ModuleProtected Module Utilities	#tag Method, Flags = &h0		Sub deleteContentsOfFolder(folder as FolderItem)		  // Code from http://ramblings.aaronballman.com/2005/04/How_to_Delete_a_Folder.html		  		  dim i, count as Integer		  count = folder.Count		  		  for i = 1 to count // Check to see if the item is a directory		    if folder.TrueItem( 1 ).Directory then		      deleteContentsOfFolder( folder.TrueItem(1) )		    end if		    folder.TrueItem( 1 ).Delete		  next i		  		End Sub	#tag EndMethod	#tag Method, Flags = &h0		Function normaliseFilePath(filePath as String) As String		  #if TargetMacOS		    return filePath.replaceAll(":", "/")		  #elseif TargetWin32		    return filePath.replaceAll("\", "/")		  #else		    return filePath		  #endif		  		End Function	#tag EndMethod	#tag Method, Flags = &h0		Function binToHex(binaryString as string, separator as string = " ") As string		  dim result as string		  dim i as integer		  		  result = ""		  For i = 1 to LenB(binaryString)		    result = result + Right("0" + Hex(Asc(MidB(binaryString, i, 1))), 2) + separator		  next		  		  return result		End Function	#tag EndMethod	#tag Method, Flags = &h0		Function hexToBin(hexString as String, separator as string = " ") As string		  dim result as string		  dim i as integer		  dim characterLength as integer		  		  characterLength = len(separator) + 2		  		  result = ""		  for i = 1 to Len(hexString) step characterLength		    result = result + Chr(Val("&h" + MidB(hexString, i, 2)))		  next		  		  return result		End Function	#tag EndMethod	#tag ViewBehavior		#tag ViewProperty			Visible=true			Group="ID"			InheritedFrom="Object"		#tag EndViewProperty		#tag ViewProperty			Visible=true			Group="ID"			InitialValue="-2147483648"			InheritedFrom="Object"		#tag EndViewProperty		#tag ViewProperty			Visible=true			Group="ID"			InheritedFrom="Object"		#tag EndViewProperty		#tag ViewProperty			Visible=true			Group="Position"			InitialValue="0"			InheritedFrom="Object"		#tag EndViewProperty		#tag ViewProperty			Visible=true			Group="Position"			InitialValue="0"			InheritedFrom="Object"		#tag EndViewProperty	#tag EndViewBehaviorEnd Module#tag EndModule