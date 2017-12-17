## INFO ##
## INFO ##

cd nordvpn;
dub build --compiler=ldc --build=release;
cd ..;

cd ufwrules;
dub build --compiler=ldc --build=release;
cd ..;
