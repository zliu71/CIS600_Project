pragma solidity >=0.4.16 <0.8.0;
/*
Zhiguang Liu
zliu71@syr.edu
Project
*/
contract DFS { 
    
    mapping (string => string) public files;
    
    string buf;
    
    function popFiles(string memory name) public returns (string memory){
        
        buf = files[name];
        return buf;
        
    }

    function pushFiles(string memory name, string memory hash) public{
        
        files[name] = hash;
        
    }
    
}
