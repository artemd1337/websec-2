import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import 'bootstrap/dist/css/bootstrap.min.css';
import styled from 'styled-components';
import {useEffect, useState} from "react";
import axios from "axios";
import './TimeTable.css'
import InfoBlock from "./InfoBlock";
import TableHeaderBlock from "./TableHeaderBlock";
import SelectRow from "./SelectRow";


const StyledCol = styled(Col)`
  border: 1px solid;
  border-color: #a6d5fa;
  text-align: center;
  flex: 1;
  min-width: 10%;
  max-width: 15%;
  flex-wrap: nowrap;
`;

const Lesson = styled(Col)`
  text-align: left;
`;


function TimeTable({category, setCategory, objectId, setObjectId, week, setWeek}) {
    let [objectName, setObjectName] = useState(null);
    let [objectDescription, setObjectDescription] = useState(null);
    let [times, setTimes] = useState(null);
    let [header, setHeader] = useState(null);
    let [lessons, setLessons] = useState(null);

    useEffect(() => {
        if (week) {
            axios.get("http://localhost:5000/api/get_timetable_lk/", {params: {
                    category: category,
                    id: objectId,
                    week: week
                }
        }).then(res => {
            setObjectName(res.data.info.object_name);
            setObjectDescription(res.data.info.object_info);
            setTimes(res.data.times);
            setHeader(res.data.header);
            setLessons(res.data.lessons);
        })
        }

    }, [category, objectId, week]);

    function TeacherClicked(teacherId){
        setCategory("staff");
        setObjectId(teacherId);
    }

    function GroupClicked(groupId){
        setCategory("group");
        setObjectId(groupId);
    }

    return (
        <>
            <InfoBlock objectName={objectName} objectProperties={objectDescription}/>
            <SelectRow setObjectId={setObjectId} setCategory={setCategory}/>
            <TableHeaderBlock week={week} setWeek={setWeek}/>
            <Container fluid className="schedule w-100">
                <Row>
                    {header && header.map(header_elem => (
                        <StyledCol key={header_elem[0]}>
                            <p className="weekday_info">{header_elem[0]}</p>
                            {header_elem.length === 2 && (
                                <p className="date_info">{header_elem[1]}</p>
                                )}
                        </StyledCol>
                    ))}
                </Row>
                {times && times.map((time, row_index) => (
                    <Row key={time}>
                        <StyledCol>
                                <p className="date_info">{time[0]}</p>
                                <p className="date_info">{time[1]}</p>
                        </StyledCol>
                        {Array.from({length: 6}).map((_, index) => (
                            <>
                            {lessons[row_index * 6 + index] && (
                            <StyledCol key={row_index * 6 + index}>
                                <Lesson>
                                    {lessons[row_index * 6 + index].subject && (
                                        <p className="subject">
                                            {lessons[row_index * 6 + index].subject}
                                        </p>
                                    )}
                                    {lessons[row_index * 6 + index].place && (
                                        <p className="place">
                                            {lessons[row_index * 6 + index].place}
                                        </p>
                                    )}
                                    {lessons[row_index * 6 + index].teacher_name && (
                                        <>
                                            {lessons[row_index * 6 + index].teacher_link &&
                                                (<a className="teacher" onClick={()=> TeacherClicked(lessons[row_index * 6 + index].teacher_link)}>
                                                    {lessons[row_index * 6 + index].teacher_name}
                                                </a>
                                                )
                                            }
                                            {!lessons[row_index * 6 + index].teacher_link &&
                                                (<a className="teacher">
                                                    {lessons[row_index * 6 + index].teacher_name}
                                                </a>
                                                )
                                            }
                                        </>
                                    )}
                                    {lessons[row_index * 6 + index].groups && lessons[row_index * 6 + index].groups.map(group => (
                                        <p>
                                            {group.group_link && (
                                                <a className="lesson-group" onClick={()=> GroupClicked(group.group_link)}>
                                                    {group.group_name}
                                                </a>
                                            )}
                                            {!group.group_link && (
                                                <a className="lesson-group">
                                                    {group.group_name}
                                                </a>
                                            )}
                                        </p>
                                    ))}
                                </Lesson>
                            </StyledCol>
                            )}
                            </>
                        ))}
                    </Row>
                ))}
            </Container>
        </>
    );
}

export default TimeTable;