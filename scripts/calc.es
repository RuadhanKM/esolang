// GET OPERATOR
	eint^op_pos_buffer;

	func^got_op_callback^operator;
		var^op_pos^int^op_pos_buffer;
		-^op_pos^1;
		var^op^str^operator;
	end;

	func^check_op_callback^char;
		+^op_pos_buffer^1;

		match^char^+^got_op_callback;
		match^char^*^got_op_callback;
		match^char^-^got_op_callback;
		match^char^/^got_op_callback;
	end;

	forstring^cmdl_args^check_op_callback;

	+^op_pos^1;




// PARSE NUMBERS
	eint^right;
	eint^left;

	slicestringleft^right^cmdl_args^op_pos;
	-^op_pos^1;
	slicestringright^left^cmdl_args^op_pos;

	parseint^left;
	parseint^right;




// EVALUATE AND PRINT
	func^add^unused;
		+^left^right;
	end;
	func^sub^unused;
		-^left^right;
	end;
	func^mult^unused;
		*^left^right;
	end;
	func^div^unused;
		/^left^right;
	end;

	match^op^+^add;
	match^op^-^sub;
	match^op^*^mult;
	match^op^/^div;

	print^left;