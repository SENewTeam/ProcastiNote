import { Col, Container, Row } from "react-bootstrap";
import CustomNavbar from "../components/Navbar";
import { Card } from "react-bootstrap";
import Table from "react-bootstrap/Table";
import { useEffect, useState } from "react";
import { FeaturesApi, UserApi } from "../utils/requests";

const Dashboard = () => {
  const [paperData, setPaperData] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [conferences, setConferences] = useState([]);
  
  const handleLinkClick = (event) => {
    event.preventDefault();
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data1 = await UserApi.getPapers();
        
        await console.log(data1)
        if (data1["message"] == "Papers : ") {
          const data2 = [
            {
              id: 1,
              title: 'Start Reading...',
              description: 'Enjoy your journey......',
              link: 'http://localhost:5173/dashboard',
            }
          ]
          setPaperData(data2);
          return;
        }
        // const data = []
        
        const data = Object.keys(data1).map( (d)=> ({
            id : d,
            title : data1[d][0],
            description : data1[d][1],
            link : "http://localhost:5173/paper/" + d 
        }))
        setPaperData(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();

    UserApi.getRecommendations()
      .then((data) => {
        console.log(data);
        setRecommendations(data);
      })
      .catch((err) => {
        console.log(err);
      });

    FeaturesApi.conferences()
      .then((data) => {
        console.log(data);
        setConferences(data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <>
      <CustomNavbar />

      <Container fluid className="mb-5">
        <h2 style={{margin:'20px'}}>Recently read by you:</h2>
        <Row className="mx-2">
          {paperData.map((card) => (
            <Col key={card.id} sm={12} md={6} lg={3} xxl={2}>
              <Card style={{ height: "100%" }}>
                <Card.Body style={{ display: 'flex', flexDirection: 'column' }}>
                  <Card.Title>{card.title}</Card.Title>
                  <Card.Text className="card-description" style={{ flexGrow: 1 }}>
                    {card.description}
                  </Card.Text>
                  <Card.Link style={{ textDecoration: 'none' }} href={card.link} target="_blank">
                    Continue Reading...
                  </Card.Link>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </Container>
      <Container fluid>
        <h2 style={{margin:'20px'}}>Recommended for you:</h2>
        <Row className="mx-2">
          {recommendations.map((card) => (
            <Col key={card.id} sm={12} md={6} lg={3} xxl={2}>
              <Card style={{ height: "100%"  }}>
                <Card.Body style={{ display: 'flex', flexDirection: 'column' }}>
                  <Card.Title>{card.title}</Card.Title>
                  <Card.Text className="card-description" style={{ flexGrow: 1 }}>
                    {card.abstract}
                  </Card.Text>
                  <a style={{ textDecoration: 'none' }} href={"http://localhost:5173/paper/" + card.paperId} target="_self" >Continue Reading...</a>

                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </Container>
      <Container fluid>
        <h2 style={{margin:'20px'}}>Conferences:</h2>
        <Table responsive className="mx-2">
          <thead>
            <tr>
              <th style={{backgroundColor:"#011638", color:"#FCBA50"}}>#</th>
              <th style={{backgroundColor:"#011638", color:"#FCBA50"}}>Conference Name</th>
              <th style={{backgroundColor:"#011638", color:"#FCBA50"}}>Deadline</th>
              <th style={{backgroundColor:"#011638", color:"#FCBA50"}}>Venue</th>
              <th style={{backgroundColor:"#011638", color:"#FCBA50"}}>Conference Link</th>
            </tr>
          </thead>
          <tbody>
            {conferences.map((conference, i) => (
              <tr key={conference.conference_id}>
                <td style={{backgroundColor:"#F8F7F7", color:"#011638"}}>{i + 1}</td>
                <td style={{backgroundColor:"#F8F7F7", color:"#011638"}}>{conference.conference_name}</td>
                <td style={{backgroundColor:"#F8F7F7", color:"#011638"}}>{conference.deadline}</td>
                <td style={{backgroundColor:"#F8F7F7", color:"#011638"}}>{conference.venue}</td>
                <td style={{backgroundColor:"#F8F7F7", color:"#011638"}}><a href={`http://www.wikicfp.com${conference.conference_link}`} rel="noreferrer" target="_blank">Link</a></td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>
    </>
  );
};

export default Dashboard;
