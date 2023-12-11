import {useEffect, useState} from "react";
import axios from "axios";

function SelectRow({setObjectId, setCategory}) {
    let [searchString, setSearchString] = useState('');
    let [searchResult, setSearchResult] = useState([]);
    useEffect(() => {
        axios("http://localhost:5000/api/search", {params:{'text': searchString}}).then(res => {
            setSearchResult(res.data);
        })
    }, [searchString]);


    const SearchStringChanged = (message) => {
    setSearchString(message.target.value);
    };

    function newObjectClicked(objectId, category){
        setCategory(category);
        setObjectId(objectId);
        setSearchString('');
    }

    return (
        <div className="search_block">
            <input className="selection_field" type="search" value={searchString} onChange={SearchStringChanged}/>
            <ul>
                {searchResult && searchResult.map(result => (
                    <li key={result.key}><a onClick={()=> newObjectClicked(result.id, result.category)}>
                        {result.name}
                    </a></li>
                ))}
            </ul>
        </div>
    );
}

export default SelectRow;