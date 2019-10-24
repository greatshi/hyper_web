pragma solidity ^0.4.10;

contract WebDefend{

    struct WebTx{
        address sender;
        string page_hash;
        string page_name;
        string last_page_hash;
        uint timestamp;
    }
    mapping(string => WebTx[]) webTxListDict;

    function sendWebTx(string _page_hash, string _page_name, string _last_page_hash, uint timestamp) public returns(string) {
        address sender = msg.sender;
        webTxListDict[_page_name].push(WebTx(sender, _page_hash, _page_name, _last_page_hash, timestamp));
        return "ok";
    }

    function getWebTx(string _page_name) public returns(address, string, string, string, uint){
        WebTx webTx = webTxListDict[_page_name][webTxListDict[_page_name].length-1];
        return (webTx.sender, webTx.page_hash, webTx.page_name, webTx.last_page_hash, webTx.timestamp);
    }
}
