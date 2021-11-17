Search.setIndex({docnames:["developer/guides/creating-commands","developer/guides/creating-parameters","developer/guides/index","developer/guides/working-with-models","developer/index","developer/reference/arguments","developer/reference/commands","developer/reference/exceptions","developer/reference/index","developer/reference/params","developer/reference/parser","developer/reference/program","index","user/index","user/lib-eems-basic","user/lib-eems-csv","user/lib-eems-fuzzy","user/lib-eems-netcdf","user/libraries-ref"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["developer/guides/creating-commands.rst","developer/guides/creating-parameters.rst","developer/guides/index.rst","developer/guides/working-with-models.rst","developer/index.rst","developer/reference/arguments.rst","developer/reference/commands.rst","developer/reference/exceptions.rst","developer/reference/index.rst","developer/reference/params.rst","developer/reference/parser.rst","developer/reference/program.rst","index.rst","user/index.rst","user/lib-eems-basic.rst","user/lib-eems-csv.rst","user/lib-eems-fuzzy.rst","user/lib-eems-netcdf.rst","user/libraries-ref.rst"],objects:{"":[[14,0,1,"","ADividedByB"],[14,0,1,"","AMinusB"],[14,0,1,"","Copy"],[16,0,1,"","CvtFromFuzzy"],[16,0,1,"","CvtToBinary"],[16,0,1,"","CvtToFuzzy"],[16,0,1,"","CvtToFuzzyCat"],[16,0,1,"","CvtToFuzzyCurve"],[16,0,1,"","CvtToFuzzyCurveZScore"],[16,0,1,"","CvtToFuzzyMeanToMid"],[16,0,1,"","CvtToFuzzyZScore"],[17,0,1,"","EEMSRead"],[17,0,1,"","EEMSWrite"],[16,0,1,"","FuzzyAnd"],[16,0,1,"","FuzzyNot"],[16,0,1,"","FuzzyOr"],[16,0,1,"","FuzzySelectedUnion"],[16,0,1,"","FuzzyUnion"],[16,0,1,"","FuzzyWeightedUnion"],[16,0,1,"","FuzzyXOr"],[14,0,1,"","Maximum"],[14,0,1,"","Mean"],[14,0,1,"","Minimum"],[14,0,1,"","Multiply"],[14,0,1,"","Normalize"],[14,0,1,"","NormalizeCat"],[14,0,1,"","NormalizeCurve"],[14,0,1,"","NormalizeCurveZScore"],[14,0,1,"","NormalizeMeanToMid"],[14,0,1,"","NormalizeZScore"],[14,0,1,"","PrintVars"],[14,0,1,"","Sum"],[14,0,1,"","WeightedMean"],[14,0,1,"","WeightedSum"]],"mpilot.arguments":[[5,2,1,"","Argument"],[5,2,1,"","ListArgument"]],"mpilot.arguments.Argument":[[5,3,1,"","lineno"],[5,3,1,"","name"],[5,3,1,"","value"]],"mpilot.arguments.ListArgument":[[5,3,1,"","list_linenos"]],"mpilot.commands":[[6,2,1,"","Command"]],"mpilot.commands.Command":[[6,3,1,"","allow_extra_inputs"],[6,4,1,"","execute"],[6,4,1,"","get_argument_value"],[6,3,1,"","inputs"],[6,3,1,"","metadata"],[6,3,1,"","output"],[6,3,1,"","result"],[6,4,1,"","run"],[6,4,1,"","validate_params"]],"mpilot.exceptions":[[7,2,1,"","CommandDoesNotExist"],[7,2,1,"","DuplicateResult"],[7,2,1,"","InvalidRelativePath"],[7,2,1,"","MPilotError"],[7,2,1,"","MissingParameters"],[7,2,1,"","NoSuchParameter"],[7,2,1,"","ParameterNotValid"],[7,2,1,"","PathDoesNotExist"],[7,2,1,"","ProgramError"],[7,2,1,"","RecursiveModelStructure"],[7,2,1,"","ResultDoesNotExist"],[7,2,1,"","ResultIsFuzzy"],[7,2,1,"","ResultNotFuzzy"],[7,2,1,"","ResultTypeNotValid"]],"mpilot.params":[[9,2,1,"","BooleanParameter"],[9,2,1,"","DataParameter"],[9,2,1,"","DataTypeParameter"],[9,2,1,"","ListParameter"],[9,2,1,"","NumberParameter"],[9,2,1,"","Parameter"],[9,2,1,"","PathParameter"],[9,2,1,"","ResultParameter"],[9,2,1,"","StringParameter"],[9,2,1,"","TupleParameter"]],"mpilot.params.Parameter":[[9,4,1,"","clean"]],"mpilot.parser":[[10,1,0,"-","parser"]],"mpilot.parser.parser":[[10,2,1,"","ArgumentNode"],[10,2,1,"","CommandNode"],[10,2,1,"","ExpressionNode"],[10,2,1,"","Parser"],[10,2,1,"","ProgramNode"]],"mpilot.parser.parser.ArgumentNode":[[10,3,1,"","lineno"],[10,3,1,"","name"],[10,3,1,"","value"]],"mpilot.parser.parser.CommandNode":[[10,3,1,"","arguments"],[10,3,1,"","command"],[10,3,1,"","lineno"],[10,3,1,"","result_name"]],"mpilot.parser.parser.ExpressionNode":[[10,3,1,"","lineno"],[10,3,1,"","value"]],"mpilot.parser.parser.Parser":[[10,4,1,"","parse"]],"mpilot.parser.parser.ProgramNode":[[10,3,1,"","commands"],[10,3,1,"","version"]],"mpilot.program":[[11,5,1,"","EEMS_CSV_LIBRARIES"],[11,5,1,"","EEMS_NETCDF_LIBRARIES"],[11,2,1,"","Program"]],"mpilot.program.Program":[[11,4,1,"","add_command"],[11,3,1,"","command_library"],[11,3,1,"","commands"],[11,4,1,"","find_command_class"],[11,4,1,"","from_source"],[11,4,1,"","load_commands"],[11,4,1,"","run"],[11,4,1,"","to_file"],[11,4,1,"","to_string"],[11,3,1,"","working_dir"]],mpilot:[[5,1,0,"-","arguments"],[6,1,0,"-","commands"],[7,1,0,"-","exceptions"],[9,1,0,"-","params"],[11,1,0,"-","program"]]},objnames:{"0":["py","function","Python function"],"1":["py","module","Python module"],"2":["py","class","Python class"],"3":["py","attribute","Python attribute"],"4":["py","method","Python method"],"5":["py","data","Python data"]},objtypes:{"0":"py:function","1":"py:module","2":"py:class","3":"py:attribute","4":"py:method","5":"py:data"},terms:{"0":[14,16],"1":[13,14,16],"10":[13,14],"12":13,"2":[0,6,10,13,14],"3":[5,10,13],"4":[5,13,14],"5":[0,5,13],"6":14,"667":14,"7":13,"8":[13,14],"boolean":[14,16],"break":0,"case":[0,13],"class":[0,1,3,5,6,7,9,10,11],"default":[0,3,6,11,14,15,16,17],"do":[4,13],"float":[9,13,15,17],"function":4,"import":[0,1,3,11],"int":[5,6,7,9,10,11],"new":[0,2,13,17],"return":[0,1,3,6,10,11],"super":1,"true":[6,9,13,14,16],"while":13,A:[0,3,7,9,10,11,14,15,16,17],AND:16,As:[0,3],At:3,Be:0,By:0,For:[3,5,6,9,13,16],If:[1,3,4,9,11,13,14,15,16,17],In:0,It:[0,4,6,10,13],NOT:16,Near:6,OR:16,One:13,The:[0,3,5,6,7,9,10,11,12,14,15,16,17],These:[13,14],Will:10,With:13,__init__:1,a_fz:13,about:[4,13],abov:[0,1],accept:[0,1,6,9],access:6,accord:10,account:0,across:11,ad:6,add:[0,1,3,11],add_command:[3,11],addit:3,addnumb:0,address:3,adividedbyb:14,against:9,aggreg:14,all:[3,9,13,14,16],allow_extra_input:6,alreadi:[4,6,9,13,15,17],also:[3,13],aminusb:14,an:[0,1,2,7,11,12,13,14,16,17],ani:[0,3,5,6,7,9,11,13,14,15,16,17],anoth:[0,1,13],appear:[5,11],appli:13,appropri:[6,11],ar:[0,3,4,6,9,10,11,12,13,17],argument:[0,1,3,4,6,7,8,9,10,11],argumentnod:10,arithmet:14,arrai:[0,13,14,15,16,17],assign:[3,10],assum:4,attribut:0,avail:3,b:[0,13,14],b_fz:13,back:3,bar:1,base:[3,7,9,11,12,14,16],basic:[13,18],becom:13,been:[0,3,6],befor:11,begin:10,being:11,between:[13,14],binari:16,bisect:16,blank:3,blue:13,bool:[6,9],booleanparamet:9,both:13,bottom:12,build:[3,11],built:[1,3,18],c:[4,13],call:[3,6,11,13],can:[0,1,3,4,6,9,11,13,15,17],cannot:9,caus:[0,9],chang:0,charact:13,check:9,circular:7,classmethod:11,clean:[1,6,9],cli:3,code:[1,4,11,12],collect:12,colon:13,color:13,colormap:6,column:[13,15],combin:13,come:13,comma:13,command:[1,2,4,7,8,10,11,12,14,15,16,17],command_cl:11,command_librari:11,commanda:13,commanddoesnotexist:7,commandnod:10,compris:11,comput:[4,13],configur:1,connect:0,consist:[13,16],construct:11,constructor:3,contain:[3,7,11,13,14,15,17,18],content:3,convers:13,convert:[0,13,14,15,16,17],copi:14,correct:10,could:[1,3,5,7],cover:[4,13],creat:[2,4,11,12,13,14,15,16,17],csv:[3,6,11,13,17,18],current:[12,13],curv:[14,16],custom:[1,3,4],cvtfromfuzzi:16,cvttobinari:16,cvttofuzzi:[13,16],cvttofuzzycat:16,cvttofuzzycurv:16,cvttofuzzycurvezscor:16,cvttofuzzymeantomid:16,cvttofuzzyzscor:16,data:[3,4,7,9,14,15,16,17],dataparamet:[0,6,9],dataset:17,datatyp:[13,15,17],datatypeparamet:9,debug:14,decim:13,deep:0,def:[0,1],defaultfuzzyvalu:16,defaultnormalvalu:14,defin:[0,3,6,14,16],del:3,delet:3,denomin:14,denot:9,depend:[3,11],deriv:14,describ:3,descript:6,determin:[3,10,13,14,16],dict:[6,9,11],dictionari:[3,6,9,11],differ:[0,1,13,15,17],dimensionfieldnam:17,dimensionfilenam:17,direct:16,directli:[3,6],directori:[3,7,11],dirnam:3,discov:11,discuss:0,displaynam:6,divid:12,document:[4,13],doe:[7,10],doesn:[7,11],don:1,done:13,down:0,duplicateresult:7,dure:9,e:[3,5,9,10,11,13,14],each:[3,5,13,14,16],easi:13,eem:[3,10,11,12,13,18],eems_csv_librari:[3,11],eems_netcdf_librair:3,eems_netcdf_librari:[3,11],eemsread:[3,6,11,13,15,17],eemswrit:[13,15,17],either:[9,10,13,15,16],emd:12,empti:[0,3],encount:3,endval:14,environment:12,equival:[3,11],error:11,essenti:16,evalu:12,exampl:[0,1,3,5,6,9],except:[0,1,3,4,8,11],execut:[0,3,6,9],exist:[7,9,11,13,14,15,17],expect:[0,6],explicitli:6,express:[10,13],expressionnod:10,extend:1,extens:12,extra:[1,4,6,13],f:3,fail:9,fairli:0,fals:[0,6,9,13,14,16],falsest:16,falsethreshold:[13,16],falsethresholdzscor:14,familiar:4,fast:1,file:[0,2,5,7,10,11,14,15],file_or_path:11,find:[3,4,13],find_command_class:[3,11],first:[0,3,11,13],focu:3,follow:[3,13,18],foo:1,foobar:1,foobarparamet:1,form:[11,13],format:[3,11],found:7,framework:12,from:[0,1,2,6,10,11,13,14,15,16,17],from_sourc:[3,11],full:[0,13],fuzzi:[7,9,12,13,14,17,18],fuzzyand:16,fuzzynot:16,fuzzyor:16,fuzzyselectedunion:16,fuzzyunion:[13,16],fuzzyvalu:16,fuzzyweightedunion:16,fuzzyxor:16,g:[3,5,9,10,11,13,14],get:0,get_argument_valu:6,given:[7,11],good:[14,16],grammar:10,graph:7,guid:[3,4,12],ha:[0,3],handl:10,hard:1,hasn:6,have:[0,3,7,11,13],help:13,here:0,high:12,highest:14,hightolow:16,hook:6,how:13,i:[13,18],ignor:[14,16],ignorezero:[14,16],implement:[1,4,6,12],improv:12,includ:[3,6,13,14],incom:[1,15,17],index:[14,16],indic:[0,6,15,17],individu:6,infieldnam:[0,3,5,6,11,13,14,15,16,17],infilenam:[3,6,11,13,15,17],inform:[4,13],initi:12,input:[0,1,3,6,9,11,13,14,16],instanc:[3,11],instead:3,integ:[9,13,14,15,16,17],integr:4,intend:[12,13],intern:11,interpol:[13,14,16],invalid:[1,7,11],invalidrelativepath:7,involv:1,io:3,is_fuzzi:9,item:[5,9],its:0,itself:[5,12],kei:[3,9,13],keyword:6,kwarg:[0,1,6,9],languag:13,latter:10,leaf:11,left:11,less:16,let:[0,1,3],level:12,lex:10,li:0,librari:[3,4,7,11,12,14,15,16,17],like:[0,5,10],limit:13,line:[5,10,11,13],linear:[14,16],lineno:[1,5,6,7,9,10,11],list:[1,5,6,9,10,11,14,15,16,17],list_lineno:5,listargu:5,listparamet:[0,9],ll:[0,3,13],load:[2,11,13,15,17],load_command:11,logic:[12,13],look:[3,5,11],lookup:11,lower:1,lowest:14,lowtohigh:16,mai:[11,13],make:13,mani:0,map:[14,16],mark:0,mask:[15,17],match:[14,16],maximum:[14,16],mean:[6,13,14,16],memoiz:6,messag:7,metadata:6,method:[0,1,3,6,11],might:[0,5],minimum:[3,14,16],miss:[0,7,15,17],missingparamet:7,missingv:[15,17],model:[0,2,4,6,7,9,11,12,13],model_path:3,modifi:[1,2,4],modul:[0,3,4,11,12],more:[4,7,13,15,17],mostli:[3,11],mpilot:[0,1,2,8],mpiloterror:7,mpt:[3,13],multipl:[13,14,15,17],multipli:14,must:[0,3,11,13,14,16],must_exist:[6,9],mycommand:1,myproject:3,n:16,name:[2,3,5,6,7,10,11,13,15,17],narmal:14,natur:11,necessari:[1,3],need:[0,1,3,12,13],nest:0,netcdf:[3,4,11,13,18],newer:13,node:[10,11],non:[7,9,14,16],none:[1,3,5,6,7,9,11],normal:[13,14,16],normalizecat:14,normalizecurv:14,normalizecurvezscor:14,normalizemeantomid:14,normalizezscor:14,normalvalu:14,nosuchparamet:7,note:0,now:[0,1,13],number:[0,9,10,11,14,15,16,17],numberparamet:[0,9],numbertoconsid:16,numer:14,numpi:0,o:18,object:[3,9],obtain:11,occur:11,occurr:[15,17],old:13,omit:3,onc:[3,6,7,13],one:[14,15,16,17],ones:14,onli:1,open:3,oper:[14,16],option:[2,3,5,6,7,9,11,13,14,15,16,17],order:4,os:3,other:[4,11,13],otherwis:14,out:[4,13],outfieldnam:[13,15,17],outfilenam:[13,14,15,17],output:[0,6,9,13],output_typ:9,overrid:1,overwritten:[14,15,17],own:[0,1],p:[3,11],packag:[4,12],page:0,pair:13,param:[0,1,4,6,8,13],paramet:[2,4,5,6,7,9,10,11,14,15,16,17],parameternotvalid:[1,7],pars:[3,4,10],parser:[4,8],particular:0,pass:[0,1,3,6,9,10],path:[3,7,9,11,14,15,17],pathdoesnotexist:7,pathparamet:[6,9],peopl:12,perform:[14,16],pip:[4,13],piyg:6,plan:[4,13],point:9,posit:17,possibl:13,present:9,previou:[0,3,13],primari:11,print:14,printvar:14,process:[13,14],produc:[0,13,14,16],program:[1,3,4,6,7,8,9,10,12],programerror:7,programm:12,programmat:[3,11],programnod:10,proper:10,properti:[0,3,6],provid:[0,1,3,7,14],purpos:14,python:[3,4,11,12,13],quickli:13,quot:13,rais:[1,11],rang:14,rather:1,raw:9,rawvalu:[14,16],read:[3,13,15,17],read_cl:11,recurs:11,recursivemodelstructur:7,refer:[4,7,12,13],referenc:[0,3,7],rel:[3,7,11],relat:16,report:11,repres:3,represent:3,requir:[0,4,7,9,11,13],required_typ:7,resolv:[3,10,11],resourc:12,respect:[14,15,17],respons:[10,11],restrict:1,result:[3,6,7,9,10,11,14,15,16,17],result_nam:[6,10,11],resultdoesnotexist:7,resultisfuzzi:7,resultnotfuzzi:7,resultparam:13,resultparamet:[0,9],resulttypenotvalid:7,revers:[0,16],road:6,root:11,run:[2,4,6,9,11,12,13],s:[0,1,3,6,9,11,17],sai:3,same:[3,7,11,13,14,15,16,17],scope:[4,13],score:[14,16],sd:6,search:11,second:3,section:[3,12],see:[0,1],self:[0,1],sent:11,separ:13,sequenc:[7,11],serial:3,set:[0,3,6,7,11],sever:[13,14],should:[0,1,4,6,11,13],side:11,similar:13,simpl:[0,3],simpli:6,singl:[15,17],size:[14,16],slow:1,so:[0,11],softwar:[4,12],some:[3,13],sourc:[2,5,10,11],space:[13,16],spec:10,specif:[13,14,16],specifi:[7,11,14,16],speed:1,start:0,startval:14,stdout:14,str:[5,6,7,9,10,11],string:[3,11,15,16,17],stringparamet:[1,6,9],structur:[10,13],sub:11,subclass:1,suit:1,sum:[0,14],sumnumb:0,support:10,sure:0,surround:13,syntax:[10,11],system:12,t:[0,1,6,7,11],take:[0,3,13],task:0,templat:17,text:10,textio:11,than:[1,7,16],thei:[0,11,13,14],them:3,thi:[0,1,3,4,5,6,9,10,11,12,13,14,15,16,17],thing:10,those:[11,13,14,16],threshold:[6,16],time:0,to_fil:[3,11],to_str:[3,11],togeth:14,too:[0,3],top:0,transform:[1,9,14,16],treat:13,tree:[3,11],truest:16,truestorfalsest:16,truethreshold:[13,16],truethresholdzscor:14,tupleparamet:9,turn:11,two:[0,3,11,12,13],type:[0,1,4,5,6,9,10,11,15,17],understand:13,union:[7,11,13,16],uniqu:[11,14,16],unmodifi:[1,6],until:11,up:[3,11,12,13],us:[0,1,3,4,6,7,9,10,11,13,14,15,16,17],user:[12,14,16],util:14,v1:10,valid:[0,1,5,6,7,9,10,13,17],valid_typ:9,validate_param:6,valu:[0,1,5,6,7,9,10,13,14,15,16,17],value_typ:9,var_a:[3,5,6,11],var_b:5,var_c:5,variabl:[13,15,17],version:[10,12,13],wa:[7,12],want:3,we:[0,1,13],weight:[14,16],weightedmean:14,weightedsum:14,well:13,when:[1,6,9,11,13,14,16],where:[3,10,14],whether:3,which:[0,3,7,9,11,12,13,14,15,16,17],who:12,without:13,word:13,work:[0,2,4,7,11],workflow:12,working_dir:[3,11],would:0,write:[3,4,11,13,14,15,17],written:14,xor:16,you:[1,3,4,13],your:[0,1,4,13],z:[14,16],zscorevalu:[14,16]},titles:["Creating Commands","Creating Parameters","Programming Guides","Working with Models","Developer Resources","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">mpilot.arguments</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">mpilot.commands</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">mpilot.exceptions</span></code>","Python Module Reference","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">mpilot.params</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">mpilot.parser.parser</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">mpilot.program</span></code>","MPilot Documentation","User Guide","EEMS Basic","EEMS CSV I/O","EEMS Fuzzy","EEMS NetCDF I/O","MPilot Libraries Reference"],titleterms:{"boolean":13,"new":3,A:13,In:13,The:13,ad:3,an:3,argument:5,basic:14,built:13,command:[0,3,6,13],content:[4,12],creat:[0,1,3],csv:15,data:13,develop:[4,12],document:12,eem:[14,15,16,17],exampl:13,except:7,file:[3,13],from:3,fuzzi:16,guid:[2,13],i:[15,17],instal:[4,13],librari:[13,18],list:[0,13],load:3,model:3,modifi:3,modul:8,mpilot:[3,4,5,6,7,9,10,11,12,13,18],name:0,netcdf:17,number:13,o:[15,17],option:[0,1],param:9,paramet:[0,1,13],parser:10,path:13,program:[2,11,13],python:8,quick:13,refer:[8,18],remov:3,resourc:4,result:[0,13],run:3,sourc:3,string:13,syntax:13,tabl:[4,12],tupl:13,type:13,us:12,user:13,work:3}})