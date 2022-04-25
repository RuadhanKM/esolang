print^;

// Get script
estr^target-file;
input^target-file:\s^target-file;
estr^args;
input^bf-input:\s^args;
var^path^str^bf-scripts/;
+^path^target-file;
estr^script;
file^path^script;
eint^len_script;
eint^len_args;
len^len_args^args;
len^len_script^script;
-^len_script^1;

print^;
print^Init\smemory...;

// Init memory
eint^pointer;
eint^inputpointer;
earr^memory;
func^add_memslot_callback^i;
	var^c^int^0;
	append^memory^c;
end; for^30000^add_memslot_callback;
earr^par_stack;
earr^matching_par;
eint^gloi;

print^Done!;

func^left^x;
	-^pointer^1;
end;
func^right^x;
	+^pointer^1;
end;

func^inc^x;
	eint^newval;
	slice^newval^memory^pointer;
	
	+^newval^1;
	%^newval^256;

	setslice^memory^pointer^newval;
end;
func^dec^x;
	eint^newval;
	slice^newval^memory^pointer;
	
	-^newval^1;
	%^newval^256;

	setslice^memory^pointer^newval;
end;

func^doin^x;
	estr^input_pointerval;
	slice^input_pointerval^args^inputpointer;
	
	ord^input_pointerval^input_pointerval;
	setslice^memory^pointer^input_pointerval;
	
	+^inputpointer^1;
end;
func^in^x;
	ebool^idk;
	<^idk^inputpointer^len_args;
	if^doin^idk;
end;
func^out^x;
	estr^c;
	
	estr^pointerval;
	slice^pointerval^memory^pointer;
	char^pointerval^pointerval;
	
	putconsole^pointerval;
end;

func^set_match_par^or;
	earr^mpbuf;
	slice^mpbuf^toret^cur_par_i;
	
	var^matching_par^arr^mpbuf;
	slice^matching_par^matching_par^0;
end;

func^search_par_open^i;
	earr^par;
	slice^par^toret^i;
	
	var^cur_par_i^int^i;
	
	eint^left_par;
	slice^left_par^par^0;
	
	match^set_match_par^left_par^gloi;
end;
func^search_par_close^i;
	earr^par;
	slice^par^toret^i;
	
	var^cur_par_i^int^i;
	
	eint^right_par;
	slice^right_par^par^1;
	
	match^set_match_par^right_par^gloi;
end;

func^skip;
	var^gloi^int^matching_par;
end;






func^par_open^x;
	for^len_toret^search_par_open;
	
	eint^pval;
	slice^pval^memory^pointer;
	eint^bruh;
	
	slice^matching_par^matching_par^1;
	
	match^skip^pval^bruh;
end;
func^par_close^x;
	for^len_toret^search_par_close;
	
	eint^pval;
	slice^pval^memory^pointer;
	eint^bruh;
	
	slice^matching_par^matching_par^0;
	
	ebool^skipcon;
	>^skipcon^pval^bruh;
	if^skip^skipcon;
end;


earr^pstack;
earr^toret;
eint^len_toret;

func^setup_par_open^x;
	append^pstack^pari;
end;
func^setup_par_close^x;
	earr^par_dict;
	eint^key;
	pop^pstack^key;
	append^par_dict^key;
	append^par_dict^pari;
	
	append^toret^par_dict;
end;



print^Getting\sloops...;

func^parentheses_callback^i;
	estr^letter;
	slice^letter^script^i;
	
	var^pari^int^i;
	
	match^setup_par_open^letter^[;
	match^setup_par_close^letter^];
end; for^len_script^parentheses_callback;

len^len_toret^toret;

var^keepcon^bool^true;
func^each_letter_callback;
	estr^letter;
	slice^letter^script^gloi;
	
	match^left^letter^<;
	match^right^letter^>;
	match^inc^letter^+;
	match^dec^letter^-;
	match^in^letter^,;
	match^out^letter^.;
	match^par_open^letter^[;
	match^par_close^letter^];
	
	+^gloi^1;
	<^keepcon^gloi^len_script;
end;

print^Done!;
print^Running\sprogram...;

print^;

while^each_letter_callback^keepcon;