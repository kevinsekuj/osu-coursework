TITLE Project Five: Arrays, Addressing, Stack-Passed Params    (Proj5_sekujk.asm)

; Author: Kevin Sekuj
; Last Modified: 3/2/21
; OSU email address: sekujk@oregonstate.edu
; Course number/section:   CS271 Section 400_W2021
; Project Number: 5               Due Date: 2/28/2021 (2 Grace days)
;
; Description: Program which generates an array of size defined by ARRAYSIZE
; and fills it with random integers within ranges defined by LO and HI, such as 
; between 10 and 29. The array is displayed as an unsorted array, and then the array
; is sorted using a sorting algorithm similar to a HLL's "bubble sort". The median of
; the array is also calculated, rounded up if necessary, and displayed. Finally, an array
; containing the count of each number in the sorted array is calculated and displayed to
; the user. This program passes parameters on the stack and uses register-indirect addressing
; for array elements.

INCLUDE Irvine32.inc

; range and array size constants
LO = 10
HI = 29
ARRAYSIZE = 220
BUFFER_SIZE = 5000

.data

; intro and title strings
intro1		byte	"	Welcome to Generating, Sorting, and Counting Random Integers, by kevin sekuj",10,13
			byte	" ",10,13
			byte	"This program generates ",0 
intro2		byte	" random numbers in the range [",0
periods		byte	" ... ",0
intro3		byte	"], displays the original list, sorts the list,",13,10
			byte	"displays the median, and then displays the list sorted in ascending order. ",10,13
			byte	" ",10,13
			byte	"Then, it displays the number of instances of each generated value, starting with the number of ",0
period		byte	"s.",0
space		byte	" ",0
median		byte	"The median value offset the array is: ",13,10,0

; arraysize set by constant 
randArray	dword	ARRAYSIZE DUP(?)

; counts array
countArray	dword	HI-LO+1 DUP(?)			; length 20 in counts array with default parameters
countSize	dword	LENGTHOF countArray		; used in final displayList call, to loop over and print elements

; array display strings
unsorted	byte	"Your unsorted random numbers:",13,10,0
medianArr	byte	"The median value of the array is: ",0
sorted		byte	"Your sorted random numbers:",13,10,0
countsTitle	byte	"Your list of instances of each generated number, starting from the value of LO:",13,10,0

;ec2
filename	byte	"rng.txt",0
buffer		byte	BUFFER_SIZE DUP(?)
fileHandle	dword	?
extra		byte	"**EC: 2. Generate numbers directly into a file, and read the file into and array.",13,10,0

.code
; ---------------------------------------------------------------------------------
; Name: main
;
; main procedure consisting of procedure calls and inline comments outlining subprocedures. 
; parameters are pushed onto the stack by value or reference depending on their type before
; each procedure call. displayList is called thrice in the program with necessary params 
; for displaying the unsorted, sorted, and count lists.
; ---------------------------------------------------------------------------------
main PROC
	call	randomize			; initialize starting seed of RandomRange proc

	push	offset	extra
	push	offset	intro1 
	push	offset	intro2 
	push	offset	intro3		
	push	offset	periods		
	push	offset	period		
	push	LO				
	push	HI					
	push	ARRAYSIZE			
	call	introduction


	push	BUFFER_SIZE			;36
	push	offset buffer		;32
	push	fileHandle			;28
	push	offset	filename	;24
	push	offset	randArray 
	push	LO		
	push	HI		
	push	ARRAYSIZE 
	call	fillArray

	push	offset	space		
	push	offset	randArray	
	push	offset	unsorted	
	push	ARRAYSIZE			
	call	displayList

	push	offset	randArray	
	push	ARRAYSIZE			
	call	sortList	
	;			exchangeElements (subProc of sortList)

	push	offset	medianArr	
	push	offset	randArray	
	push	ARRAYSIZE			
	call	displayMedian

	push	offset	space		
	push	offset	randArray	
	push	offset	sorted		
	push	ARRAYSIZE			
	call	displayList
			
	push	offset	countArray			
	push	offset	randArray			
	push	HI							
	push	LO							
	push	ARRAYSIZE					
	call	countList

	push	offset	space				
	push	offset	countArray			
	push	offset	countsTitle			
	push	countSize					
	call	displayList

	Invoke ExitProcess,0	; exit to operating system
main ENDP

; ---------------------------------------------------------------------------------
; Name: introduction
;
;	Displays program information to the user, including author, title, and the basic outline
;	of the program's function.
;
; Preconditions: none
;	
; Postconditions: none (registers preserved)
;
; Receives:
;	 intro1, intro2, intro3, periods, period, extra = strings to describe program or formatting
;	 LO = lower range limit
;	 HI = upper range limit
;	 ARRAYSIZE = constant for setting array size
;
; Returns: none
;
; ---------------------------------------------------------------------------------
introduction PROC	
	push	ebp
	mov		ebp, esp
	push	edx
	push	eax

	; display title and program prompts, also using constants in the display so
	; as not to hardcode instructions in case of changing program functionality
	mov		edx, [ebp + 36]		
	call	WriteString
	mov		eax, [ebp + 8]
	call	WriteDec

	mov		edx, [ebp + 32]		
	call	WriteString
	mov		eax, [ebp + 16]
	call	WriteDec

	mov		edx, [ebp + 24]
	call	WriteString
	mov		eax, [ebp + 12]
	call	WriteDec

	mov		edx, [ebp + 28]
	call	WriteString
	mov		eax, [ebp + 16]
	call	WriteDec

	mov		edx, [ebp + 20]
	call	WriteString
	call	CrLf
	call	CrLf

	mov		edx, [ebp + 40]
	call	WriteString
	call	CrLf

	pop		edx
	pop		eax
	pop		ebp
	ret		32
introduction ENDP

;---------------------------------------------------------------------------------
; Name: fillArray
;	Fills the buffer array using randomly generated numbers by the Irvine library's RandomRange
;	procedure. ARRAYSIZE is used as a loop counter and values are checked
;	to be within the proper constant ranges, and filled into the array via indirect register
;	addressing.
;  
;  Once the buffer array is filled, it's written into a text file. Next, the text file is opened
;  and read into randArray, which will be used in the rest of the program.
;
;
; Preconditions: Randomize has initialized random number seed, array is of type DWORD and size
; has been set to ARRAYSIZE constant's value.
;
; Postconditions: none (registers preserved)
;
; Receives:
;	 randArray = address of the array to be filled
;	 LO, HI, ARRAYSIZE = constant ranges and array size limits used to validate generated numbers
;	 and used in a loop to fill the array, respectively.
;
;	 buffer = buffer array where data is written and read from
;	 filename = name of file that data is being written to
;    filehandle = return code of various irvine procedures necessary for proper function
;
; Returns: 
;		buffer = writes and reads data from file, loads it into randArray
;		randArray = filed with random integers within constant limits
;
; ---------------------------------------------------------------------------------
fillArray PROC
	push	ebp	
	mov		ebp, esp
	pushad

	; creating output file for array values to be written into
	mov		edx, [ebp + 24]
	call	CreateOutputFile
	mov		[ebp + 28], eax


	mov		ecx, [ebp + 8]		; set ecx to ARRAYSIZE (default 200)
	mov		edi, [ebp + 32]		; address of buffer into edi for writing

_FillLoop:
	; loop for filling array with randomized values within proper ranges

	mov		eax, [ebp + 12]
	inc		eax					; to include upper limit
	call	RandomRange			; 0 - HI
	cmp		eax, [ebp + 16]		; if eax < LO, retry
	jl		_FillLoop

	mov		[edi], eax		
	add		edi, 4 				; inc by type (DWORD for current program functionality)
	loop	_FillLoop



; ----------------------------------------------------------
;  Writing array values into a file
;  
;	In the fill loop above, buffer was filled with randomly generated
; numbers within the range limits. The values are then written into a
; text file using WriteToFile, and closed with CloseFile.
;
; Next, buffer is 'reset' using a loop that moves zero into its array elements, to 
; ensure that the file's data is actually being read into buffer later on.
;
;-------------------------------------------------------------


	; moving array values in buffer to a file
	mov		eax, [ebp + 28]		; fileHandle
	mov		edx, [ebp + 32]		; buffer
	mov		ecx, [ebp + 36]		; BUFFER_SIZE

	call	WriteToFile
	mov		eax, [ebp + 28]
	call	CloseFile


	push	ecx	
	push	eax

	mov		ecx, [ebp + 8]		; set ecx to ARRAYSIZE (default 200)
	mov		edi, [ebp + 32]		; address of buffer array into edi for writing
	mov		eax, 0
_ZeroBuffer:
; "Resetting" buffer array by replacing its elements with 0s
	mov		[edi], eax		
	add		edi, 4 		
	
	loop	_ZeroBuffer
	pop		ecx
	pop		eax


;------------------------------------------------------------
;  Reading array values from a file into randArray
;  
;	The text file that was created and written to is opened using irvine
;  procs OpenInputFile, ReadFromFile, and CloseFile. Since buffer was reset
; earlier, the buffer array is now ensured to be reading from the file's
; data values. 
; 
; The buffer array is then read and written into randArray in edi, which will be
; used for the remainder of the program.
;
;-------------------------------------------------------------


	; loading data file into array
	mov		edx, [ebp + 24]		; filename
	call	OpenInputFile
	mov		[ebp + 28], eax		; filehandle

	mov		eax, [ebp + 28]		
	mov		edx, [ebp +	32]		; buffer
	mov		ecx, [ebp + 36]     ; BUFFER_SIZE
	call	ReadFromFile

	mov		eax, [ebp + 28]
	call	CloseFile


	; reading/writing into randArray
	mov		esi, [ebp + 32]		; address of buffer into esi
	mov		edi, [ebp + 20]		; address of randArray into edi
	mov		ecx, [ebp + 8]		; set ecx to ARRAYSIZE for loop

_WriteIntoArray:
; Reading data from buffer array in esi and writing it into randArray in edi

	mov		eax, [esi]		
	xchg	eax, [edi]
	add		esi, 4
	add		edi, 4

	loop	_WriteIntoArray


	popad
	pop		ebp
	ret 32
fillArray ENDP


; ---------------------------------------------------------------------------------
; Name: sortList
;	sorts the array using an unoptimized bubble-sort like algorithm. array elements are compared
;	to the next element over, and swapped if they're not in ascending order,
;	up the length of the array. 
;
; Preconditions: randArray filled with random integers and is of type DWORD. Note that this
;	procedure follows rubric/program guidelines and increments the array pointer based on
;	an array of type DWORD. 
;
; Postconditions: none (registers preserved)
;
; Receives:
;	 randArray = address of the array filled with random numbers
;	 ARRAYSIZE = constant referring to the size of randArray
;	 
; Returns: 
;	randArray = array now sorted in ascending order starting from LO value
;
; ---------------------------------------------------------------------------------
sortList PROC
    push    ebp
    mov     ebp, esp
	pushad	
        
    mov     esi, [ebp + 12]     ; address of array into esi (offset randArray)
    mov     ecx, [ebp + 8]      ; set ecx to the array's size (default 200)
	mov		ebx, [ebp + 8]		; same, but in ebx
_OuterLoop:
;  Outer nested loop where ebx is decremented. ebx acts as a second "counting" variable
; i.e 'j' in a higher level bubble sort algorithm
	mov		ebx, ecx
	dec		ebx
    mov     esi, [ebp + 12]     
    
                _InnerLoop:
				;  inner nested loop where array indices are compared 
				cmp		ebx, 0
				je		_Continue

                mov     eax, [esi]          ; i into eax
				push	esi					; preserve esi for a moment
				add		esi, 4				
				mov		edx, [esi]			; move i+1 into edx
				pop		esi					

                cmp     eax, edx           
                jg      _Exchange           ; exchange if arr[i] > arr[i+1] 

                add     esi, 4				; else, increment to next array value
				dec		ebx					; and restart
                jmp		_InnerLoop
 
                _Exchange:
				; elements that need to be swapped are pushed and exchangeElements
				; is called, a subprocedure which handles swapping
                push    eax    
				push	edx       
                call    exchangeElements
 
                add     esi, 4				; increment to to the next value when finished
                dec		ebx
				cmp		ebx, 0				; if ebx == 0, inner loop finished, loop from next value
				je		_Continue

				jmp		_InnerLoop			; else, continue inner loop
 
                _Continue:
				; label to handle looping back the outer loop 
                loop    _OuterLoop
_EndSort:
; label to handle sorting end
	popad
	pop		ebp
	ret     8
sortList ENDP

; ---------------------------------------------------------------------------------
; Name: exchangeElements (subprocedure)
;	Subprocedure of fillArray, called when two array elements are meant to be swapped.  
;	 eax and edx are pushed to the procedure, containing the elements to be swapped, and
;	swapped into the array as described in the procedure.
;
; Preconditions: arr[i] > arr[i+1], each element in eax, edx
;	
; Postconditions: eax, edx changed (pushed from sortArray)
;
; Receives: eax, edx, containing values to be swapped
;	 
; Returns: elements swapped in array 
;		
; ---------------------------------------------------------------------------------

exchangeElements PROC
	push	ebp	
	mov		ebp, esp

	mov		[esi], edx		; lower value in edx moved into array pos
	push	esi				
	add		esi, 4			; esi preserved and incremented to 
	xchg	eax, [esi]		; exchange higher value in eax into i+1
	pop		esi				

	pop		ebp
	ret 8
exchangeElements ENDP

; ---------------------------------------------------------------------------------
; Name: displayList
;	display procedure used to display the unsorted and sorted arrays, as well as the counts
;	array. The procedure is non-specific in the sense that it will display an array along
;	with its proper title as long as they are passed in the correct order.
;
; Preconditions: unsorted array is filled, sorted array is filled, or counts array is filled. 
;	Called three times during this program. Arrays are DWORD arrays.
;
; Postconditions: none (registers preserved)
;
; Receives:
;	 title of array = unsorted/sorted/counts depending on which displayList call
;	 array = either unsorted/sorted randArray or counts array
;
;	 ARRAYSIZE = size of the array used in print-looping its elements 
;	 countSize = size of count array used in print-looping
;
;	 space = string for formatting
;
; Returns: 
;	 none,  array printed to the terminal but not changed
; ---------------------------------------------------------------------------------
displayList PROC
	push	ebp
	mov		ebp, esp
	pushad
	
	; display array title
	call	CrLf
	mov		edx, [ebp + 12]
	call	WriteString

	xor		ebx, ebx
	mov		ecx, [ebp + 8]		; set ecx to array size
	mov		esi, [ebp + 16]		; array address offset into esi
_DisplayLoop:
; ebx incremented on each element printed, jumps to _NewLine 20
	cmp		ebx, 20
	je		_NewLine

_Continue:
	; looping through array elements, printing out the value and a space
	; incrementing esi by 4 (for DWORD array) 
	mov		eax, [esi]
	call	WriteDec
	mov		edx, [ebp + 20]
	call	WriteString
	inc		ebx
	add		esi, 4

	loop	_DisplayLoop
	call	CrLf
	jmp		_EndDisplay

_NewLine:
; new line when ebx is 20, clear when done to restart line counter
	call	CrLf
	xor		ebx, ebx
	jmp		_Continue

_EndDisplay:
; handle proc end
	popad
	pop		ebp
	ret	16
displayList	ENDP

; ---------------------------------------------------------------------------------
; Name: displayMedian
;	calculates and displays the median of the array, using the appropriate logic depending 
;	on whether array length is odd or even. 
;
; Preconditions: array is of type DWORD and sorted (although median printed before sorted array
;	is).
;
; Postconditions: none (registers preserved)
;
; Receives:
;	 medianArr = string to display median title
;	 randArray = array address offset
;	 ARRAYSIZE = array size 
;
; Returns: 
;	 none (median calculated and displayed to terminal, but not saved, registers preserved)
;	
; ---------------------------------------------------------------------------------

displayMedian PROC
	push	ebp
	mov		ebp, esp
	pushad

	mov		esi, [ebp + 12]		; address of array into edi
	mov		eax, [ebp + 8]
	push	eax					; preserve eax for a moment

	; if edx == 0, even length array
	mov		ebx, 2
	mov		edx, 0
	div		ebx		
	cmp		edx, 0
	je		_evenLengthArray		
	
	; median formula for odd array length, (len(arr-1) // 2
	pop		eax					
	dec		eax
	
	mov		edx, 0
	mov		ebx, 2
	div		ebx

	; mul eax by array type (DWORD) and increment esi
	; in order to get median index, move value into eax
	mov		ebx, 4				
	mul		ebx					
	add		esi, eax
	mov		eax, [esi]

	call	CrLf
	mov		edx, [ebp + 16]
	call	WriteString

	call	WriteDec
	jmp		_EndMedian

_evenLengthArray:
	; handles calculating median for arrays of even length
	; two array values at the median are added and averaged,
	; rounded up if necessary, to display median

	pop		eax				; len-1 // 2
	dec		eax

	mov		edx, 0
	mov		ebx, 2
	div		ebx	

	mov		ebx, eax		; eax = len(arr) -1 / 2
	mov		edx, eax	
	inc		edx				

	mov		ebx, 4
	mul		ebx
	add		esi, eax
	mov		eax, [esi]		; move index on the left to eax

	add		esi, 4			; increment esi and move index to the right
	mov		ebx, [esi]		; into ebx
	add		eax, ebx		

	; divide by 2
	mov		ebx, 2
	mov		edx, 0
	div		ebx

	cmp		edx, 0			; round median half up
	jne		_RoundUp

	; string for median title 
	call	CrLf
	mov		edx, [ebp + 16]
	call	WriteString
	call	WriteDec

	jmp		_EndMedian

_RoundUp:
	; handles cases where there isn't any rounding

	inc		eax
	call	CrLf
	mov		edx, [ebp + 16]
	call	WriteString
	call	WriteDec

	jmp		_EndMedian

_EndMedian:
	; handles proc end

	call	CrLf
	popad	
	pop		ebp
	ret		12
displayMedian ENDP

; ---------------------------------------------------------------------------------
; Name: countList
;	Checks the values in randArray index by index, incrementing ebx while values are equal.
;	When a different value is found, the count of that particular value is placed into 
;	countArray. During the loop, edx is initialized at the value of LO, and incremented along
;	with each value. This ensures that if a value never appears, a "0" is correctly displayed
;	and countArray is incremented to the next position. This may occur in smaller sized arrays.
;
; Preconditions: randArray is filled/sorted and of type DWORD
;	
; Postconditions: none (registers preserved)
;
; Receives:
;	 countArray = address offset of counts array
;	 randArray = address offset of sorted random number array
;	 HI	= upper value constant
;	 LO = lower value constant
;	 ARRAYSIZE = size of random number array
;
; Returns: countArray, array containing instances of each generated number 
;
; ---------------------------------------------------------------------------------

countList PROC
	push	ebp
	mov		ebp, esp
	pushad

	mov		esi, [ebp + 20]		; address of randArray into esi
	mov		edi, [ebp + 24]		; address of countArray into edi

	mov		ebx, 1
	mov		edx, [ebp + 12]		; mov LO into edx
	mov		ecx, [ebp + 8]		; set ecx to ARRAYSIZE for loop

; ----------------------------------------------------------
; Counting loop
;  
;	Checks if an element in the array is equal to the next element over,
; doing so repeatedly and increasing ebx while they are. edx holds the LO
; constant's value, to account for cases where an element never appears, such.
; as in arrays of small sizes.
; 
; edx is incremented along with each element's value. If a value is missing, 
; eax will not equal edx, and the loop will increment to the next value over
; in order to correctly place a count of "0" in that position
;
;-------------------------------------------------------------

_CountNums:
; checks an element in the array to the next elements over repeatedly
; until no longer equal. counts are inc'd in ebx

	mov		eax, [esi]			; move first array element into eax
	cmp		eax, edx
	jne		_Pass				

	add		esi, 4				; cmp to next element
	cmp		eax, [esi]
	jne		_Break
	inc		ebx					; inc count of that element 			

	loop	_CountNums
	jmp		_EndCountList

_Pass:
; increments to next position in countsArray, so that previous position is
; correctly printed as "0" for numbers that do not appear at all in the array

	add		edi, 4
	inc		edx
	jmp		_CountNums
	
_Break:
; move the count of a number (how many times it has appeared) into countArray
; and increment to next position 

	mov		[edi], ebx		
	add		edi, 4 		
	inc		edx

	mov		ebx, 1				; reset "counter"
	loop	_CountNums

_EndCountList:
; handles proc end
	pop		ebp
	popad
	ret		24 
countList ENDP

END main
