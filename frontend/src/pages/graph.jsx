import { useState } from "react";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import CustomNavbar from "../components/Navbar";
import { Container } from "react-bootstrap";
import AuthorGraph from "../components/AuthorGraph";
import CitationsGraph from "../components/CitationsGraph";
// import ReferencesGraph from "../components/ReferencesGraph";
import { useParams } from "react-router-dom";

const Graph = () => {
  const { initialPaperId } = useParams();
  const [graphBy, setGraphBy] = useState("author"); // author, citation, reference

  return (
    <>
      <CustomNavbar />
      <Container fluid style={{ height: "calc(100vh - 100px)", padding: "20px" }} onContextMenu={(e) => e.preventDefault()}>
        <Tabs
          defaultActiveKey="author"
          onSelect={key => setGraphBy(key)}
          style={{ maxHeight: "50px", justifyContent: "center" }}
        >
          <Tab eventKey="author" title="Author"></Tab>
          <Tab eventKey="citation" title="Citation"></Tab>
        </Tabs>
        <div style={{ height: "100%", position: "relative" }}>
          {(graphBy === "author") ? (
            <AuthorGraph initialPaperId={initialPaperId} />
          ) : (
            (graphBy === "citation") ? (
              <CitationsGraph initialPaperId={initialPaperId} />
            ) : (
              <div>No graph selected</div>
            )
          )}
        </div>
      </Container>
    </>
  );
};

export default Graph;
