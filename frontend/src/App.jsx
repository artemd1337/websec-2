import React, {useEffect, useState} from 'react';
import axios from "axios";
import TimeTable from "./TimeTable";

function App() {
    let [currentWeek, setCurrentWeek] = useState(null);
    let [currentCategory, setCurrentCategory] = useState("group");
    let [currentObjectId, setCurrentObjectId] = useState(531873998);
    let [weekNumber, setWeekNumber] = useState(null);
    useEffect(() => {
        axios("http://localhost:5000/api/get_current_week").then(res => {
            setCurrentWeek(res.data);
            setWeekNumber(res.data);
        })
    }, []);

    return (
        <div className="App">
            <div className='schedule'>
                <TimeTable category={currentCategory}
                           setCategory={setCurrentCategory}
                           objectId={currentObjectId}
                           setObjectId={setCurrentObjectId}
                           week={weekNumber}
                           setWeek={setWeekNumber}
                />
            </div>
        </div>
  );
}

export default App;
