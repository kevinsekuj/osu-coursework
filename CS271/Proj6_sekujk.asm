TITLE Project Six, String Primitives, Macros     (Proj6_sekujk.asm)

; Author: Kevin Sekuj
; Last Modified: 3/16/21
; OSU email address: sekujk@oregonstate.edu
; Course number/section:   CS271 Section 400_W2021
; Project Number: 6				Due Date: 3/14/21 (2 Grace Days)
;
; Description: Test program which uses two macros, GetString and DisplayString, to
; read ten signed integers from the user, and convert them to integers. The integers are
; then processed for their sum and average, and then converted back to strings
; along with their average/sum and displayed to the user. Printing values is implemented
; using the DisplayString macro. The user may lead their integers with a (+) or (-)
; sign, as well as a number of leading 0's. However, inputs above or below the
; maximum/minimum 32 bit signed integer ranges are blocked, and non-integer inputs
; like letters are also blocked.

INCLUDE Irvine32.inc

;----------------------------------------------------------------------------------
; Name: mGetString
;
; Displays a prompt asking the user for a signed integer, then gets the user's input
; and saves it into a memory address (buffer). 
;
; Preconditions: ReadVal proc is called, is passed the proper parameters such as chars
; allowed and buffer size.
;
; Receives:
; prompt = string prompting the user to enter a signed int
; buffer = input buffer, allows user to enter leading 0s
; bytesRead = user's input bytes after processed by buffer
; count = max number of characters
;
; returns: bytesRead = user input bytes
; ---------------------------------------------------------------------------------

mGetString MACRO prompt, buffer, bytesRead, count
	pushad

	mov		edi,  bytesRead
	mov		edx,  prompt
	call	WriteString

	mov		edx,  buffer		; buffer address 
	mov		ecx,  count			; max characters
	call	ReadString
	mov		[edi],	eax			; number of chars in buffer

	popad	
ENDM

;----------------------------------------------------------------------------------
; Name: mDisplayString
;
;  Basic macro for handling printing passed string parameters to the console.
;
; Preconditions: Input parameters must be specified in a memory location and pushed by 
; reference.
;
; Receives:
; output = input parameter pushed by reference
;
; returns: nothing (prints to terminal)
; ---------------------------------------------------------------------------------

mDisplayString MACRO output
	push edx

	mov		edx, output
	call	WriteString

	pop edx
endm

; Constants 

ARRAYSIZE = 10		; declaring length of the numbers array
BUFFER_SIZE = 100	; maximum buffer size allowed
CHAR_COUNT = 25		; amount of user chars allowed

.data

; Program information strings 
intro		byte	"				Welcome to String Primitives and Macros! by kevin sekuj",13,10,13,10
			byte	"Please provide 10 signed decimal integers - ",13,10,13,10
			byte	"Each integer needs to be small enough to fit inside a 32 bit register. After you've finished entering the raw",13,10
			byte	 "numbers, I'll display a list of the integers, their sum, and their average value.",13,10,13,10,0

error		byte	"ERROR: You did not enter a signed number, or your number was too large.",13,10,0
countStr	byte	"You entered the following numbers:",13,10,0
sumStr		byte	"The sum of these numbers is: ",0
avgStr		byte	"The rounded average is: ",0
space		byte	" ",0
bye			byte	"thank you, and goodbye!",13,10,0

; mGetString prompt and vars
prompt		byte	"Enter a signed number: ",0
buffer		sdword	BUFFER_SIZE DUP(?)
bytesRead	sdword	?

; Variables for handling/converting user's input 
userNum		sdword	?
numArray	sdword	ARRAYSIZE DUP(?)
numSize		dword	LENGTHOF numArray
isNegative	dword	0

; Vars used in calculations and conversion
sum			sdword	?
avg			sdword	?
count		dword	0
write		byte	BUFFER_SIZE DUP(?),0	; used in WriteVal for Int:Str conversion

.code

; ---------------------------------------------------------------------------------
; Name: main
;	main procedure containing the program's test-code. After the introduction proc,
; ReadVal is called to take and validate a user's input, which are filled into the numArray
; array. The sum and floored average of the numbers are calculated, then all three are passed
; to WriteVal to convert them to strings of ascii digits and printed.
;
; Preconditions: None
;
; Postconditions: registers eax, ebx, edx, ecx, edi, esi changed
;
; Receives: intro
;		 numArray = array containing validated user numbers
;		 numSize = LENGTHOF numArray
;		 sum = sum of user entered ints
;		 avg = floored average of user entered ints
;
; returns: numArray = array of validated SDWORDs, sum = sum of validated digits, 
;			average = floored average of validated digits
; ---------------------------------------------------------------------------------

main PROC
	
	; introduction proc displaying intro text

	push	offset intro
	call	introduction


;-----------------------------------------------------
;	Number validation and array filling
;
;	Validated user numbers are returned from ReadVal and filled into
; the numArray array via register indirect addressing. Loop counter set
; to LENGTHOF numArray.
;
;-----------------------------------------------------

	mov		edi, offset numArray
	mov		ecx, numSize			; 10 elements
_Validate:
; Numbers read from user and validated, filled into numArray 

	push	offset userNum		
	push	isNegative			
	push	offset error		
	push	CHAR_COUNT				
	push	offset bytesRead	
	push	offset	buffer		
	push	offset	prompt		
	call	ReadVal

	mov		eax, userNum
	mov		[edi], eax
	add		edi, 4
	loop	_Validate			
								


;-----------------------------------------------------
;	Sum and average calculations
;
;	Once numArray is filled with ten user input, validated numbers,
; these values are "unpacked" from the array and accumulated, saved
; in the sum variable. Uses register-indirect addressing.
;
;	Next, the sum is divided by 10, for the count of user numbers input, 
;	which returns the floored down  average. If the sum of numbers equals 0,
;	then the avg will be incremented to 1.
;
;-----------------------------------------------------

	xor		eax, eax
	xor		ebx, ebx

	mov		esi, offset numArray
	mov		ecx, numSize
_Sum:
	; Accumulate array elements via register-indirect addressing
	mov		ebx, [esi]
	cmp		ebx, 0
	add		eax, ebx
	add		esi, 4
	loop	_Sum

_Div:
	mov		sum, eax

	; divide sum by 10 
	mov		ebx, 10
	mov		edx, 0
	cdq
	idiv	ebx
	mov		avg, eax

	; if average = 0, round to 1, else break
	cmp		eax, 0
	je		_RoundZero
	cmp		eax, 0
	jmp		_Break

_RoundZero:
	; Handles rounding up to 1 in case of an average of zero
	inc		avg
	mov		eax, avg
_Break:
	; To handle end of code block


;------------------------------------------------------
;	Converting integers back to ascii strings 
;
; Once the user's input is validated and filled into an array, and
; the average/sum of their values is calculated, these values are passed
;  to the WriteVal proc to convert them back into strings using the reverse
; of the algorithm used in ReadVal. They are then displayed using mDisplayString.
;
;------------------------------------------------------
	
	call	CrLf
	mDisplayString offset countStr

	mov		esi, offset numArray
	mov		ecx, numSize
	std
_WriteLoop:
	; Passing array values to userNum variable which is pushed as an input
	; param to WriteVal, along with write, an empty array which will be filled
	; with user input integers, now strings. 

	mov		eax, [esi]
	mov		userNum, eax

	push	offset write				
	push	userNum
	call	WriteVal

	mDisplayString offset space		 ; "  " for display spacing

	add		esi, 4
	loop	_WriteLoop

	call	CrLf
	call	CrLf


	; Converting sum to string and displaying with WriteVal 
	mDisplayString offset sumStr

	push	offset write		
	push	sum					
	call	WriteVal
	call	CrLf


	; converting average to string and displaying with WriteVal
	mDisplayString offset avgStr

	push	offset write
	push	avg
	call	WriteVal
	call	CrLf

	call	CrLf

	; printing goodbye message
	mDisplayString offset bye

	Invoke ExitProcess,0	; exit to operating system
main ENDP

; ---------------------------------------------------------------------------------
; Name: introduction
;
; Displays Displays program intro to user using mGetString.
; 
; Preconditions: none
;
; Receives:
; intro = string introduction message
; ---------------------------------------------------------------------------------

introduction PROC
	push	ebp
	mov		ebp, esp

	mDisplayString [ebp+8]

	pop		ebp
	ret		8
introduction ENDP


; ---------------------------------------------------------------------------------
; Name: ReadVal
;	Procedure to read user string inputs using the mGetString macro, and then convert them to 
; strings. Values are validated on being valid numbers within the min/max range of 32 bit registers.
; Numbers are converted to strings using an algorithm which subtracts 48 from the int to get its 
; ascii value, and then multiplying it by 10, storing it in edx which holds the running total of the int.
; If the number was passed with a negative sign, a bool is set while the number is being processed, and
; it will be NEG'd at the end of the procedure.
;
; Preconditions: none
;
; Postconditions: none (Registers preserved)
;
; Receives:
;			userNum = memory variable to store validated user number
;			isNegative = bool for detecting leading (-) signs
;			error = string prompt for an invalid input
;			CHAR_COUNT = constant initialized to 25 allowing max user chars, used in mGetString
;			buffer = input buffer, allows user to enter leading 0s, used in mGetString
;			bytesRead = user's input bytes after processed by buffer, used in mGetString
;			prompt = instruction prompt used in mGetString
;
; returns: userNum = output parameter containing validated integer, converted to ascii string
; ---------------------------------------------------------------------------------

ReadVal PROC
	push	ebp
	mov		ebp, esp
	pushad	
	xor		edx, edx

_NumCheck:
	;	prompt, buffer, bytesRead, CHAR_COUNT
	mGetString	[ebp + 8], [ebp + 12], [ebp + 16], [ebp + 20]

	mov		esi, [ebp + 12]		; buffer
	push	esi
	mov		esi, [ebp + 16]		; loading bytesRead into ECX
	mov		ecx, [esi]			
	pop		esi

	cld							; clear direction flag to increment pointer
_NumLoop:
	; Validating string numbers and converting them to ints

	lodsb	

	; Validate if nums 48 <= num <= 57
	cmp		al, 2Bh				; ascii +, pass
	je		_Pass
	
	cmp		al, 2Dh				; ascii neg  
	je		_IsNegative
	cmp		al, 30h				; ascii 0
	jl		_InvalidNum
	cmp		al, 39h
	jg		_InvalidNum			; ascii 9

	sub		al, 48				; convert ascii char to int
	push	eax

	mov		eax, edx			; current total 
	mov		ebx, 10
	imul		ebx				; 10 x current total
	jc		_OutOfRange
	mov		edx, eax			; current total into edx

	pop		eax
	add		dl, al	
	
	loop	_NumLoop
	jmp		_End

_Pass:
	; Handles leading "+" and 0s

	loop _NumLoop

_IsNegative:
	; Incrementing ebx depending on neg sign

	push	eax
	mov		al, 1
	add		[ebp+28], al		; isNegative, 0 => 1
	pop		eax

	loop	_NumLoop

_InvalidNum:
	; Handles invalid numbers outside of the range 0-9 or non-numbers

	mDisplayString [ebp+24]		; print error msg
	xor		edx, edx

	jmp	_NumCheck

_OutOfRange:
	; Handles outputs that are too large/small for the 32 bit registers

	pop eax
	mDisplayString [ebp+24]
	xor		edx, edx

	jmp		_NumCheck

_End:
	; label to handle proc return

	mov		eax, [ebp+28]		; isNegative (0 or 1) 
	mov		ebx, 1
	cmp		eax, ebx
	je		_Negative

	mov		edi, [ebp+32]		; move userNum into edi
	mov		[edi], edx			; move validated number into edi value
	jmp		_Return

_Negative:
	; NEG's ints that were passed as strings with leading (-) signs

	neg		edx
	mov		edi, [ebp+32]		; move userNum into edi
	mov		[edi], edx

_Return:
	; exit proc
	popad
	pop		ebp
	ret		28
ReadVal ENDP


; ---------------------------------------------------------------------------------
; Name: WriteVal
;	Procedure used to convert user input numbers and calculated sum/average back to strings from SDWORDs
; and display them. Takes user numbers, avg, and sum as input parameters by value. The procedure reverses
; the algorithm used in ReadVal, by dividing the integers by 10 and then adding 48 to get the ascii
; values. This procedure also contains local variables negative and counter. Negative is used as a bool to
; append a negative sign (-) to negative integers.
;
;
; Preconditions: ReadVal must have been called, taking user inputs via mGetString. These inputs were validated within
; test code in main and filled into numArray, where each element is pushed to WriteVal in a loop.
;
; Postconditions: none (registers preserved)
;
; Receives:
;		write = empty byte array to receive ascii representations of SDWORDs
;		userNum = variable containing particular array element to be converted and displayed
;		avg, sum = floored average and sum of user input numbers to be converted and displayed
;
; returns: 
;		none (stores values in empty array and displays them)
;
; ---------------------------------------------------------------------------------

WriteVal PROC
	local	negative:dword, counter:dword	

	pushad
	xor		ebx, ebx
	mov		counter, 0			; initializing counter
         
	mov		eax, [ebp+8]		; num to convert
	cmp		eax, 0
	jl		_IsNegative			; jump to IsNegative label for handling negatives
	jmp		_Start

_IsNegative:
	; set negative local variable bool to 1, which will append
	; a negative sign to the value when it is printed

	mov		negative, 1
	neg		eax
_Start:
	; handle loop start

	cld							; increment pointer
_Convert:
	mov		ebx, 10        
	mov		edx, 0
	cdq
	idiv	ebx
	inc		counter				; inc counter on div to handle multi-digit numbers

	add		edx, 48
	push	edx					; store ascii value of remainder
	cmp		eax, 0     
	jnz		_Convert      


	mov		edi, [ebp + 12]		; mov empty array into edi, to be filled
_CheckNegative:
	; Check if negative bool is true

	mov		ebx, 1
	cmp		ebx, negative
	jne		_reverse			;

	mov		eax, 2Dh			; ascii negative
	stosb						
	
_Reverse:
	; reverses string due to byte ordering, decrements counter

	pop		eax					; contains remainder
	dec		counter
	stosb
	
	mov		ecx, counter
	cmp		ecx, 0			  
	je		_break				; break if counter == 0, in that case all 
								; digis of an integer have been converted in proper order
	jmp		_reverse 

_Break:
	; label to handle appending null terminator and displaying string

	mov		eax, 0			  ; string null terminating char
	stosb
	mDisplayString [ebp+12]

_End:
	; label to handle program end

	popad
	ret		8

WriteVal ENDP

END main