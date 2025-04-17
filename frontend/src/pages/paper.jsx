import { Button, Col, Container, Row, Stack } from "react-bootstrap";
import CustomNavbar from "../components/Navbar";
import Badge from "react-bootstrap/Badge";
import Form from "react-bootstrap/Form";
import Modal from "react-bootstrap/Modal";
import { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import { AlertApi, CommentsApi, UserApi } from "../utils/requests";
import AiRewrite from "../components/AiRewrite";
import swal from 'sweetalert';


const Paper = () => {
  const { id } = useParams();
  const [paperName, setPaperName] = useState("");
  const [venueType, setVenueType] = useState("");
  const [venueName, setVenueName] = useState("");
  const [venueLink, setVenueLink] = useState("");
  const [authors, setAuthors] = useState("");
  const [abstract, setAbstract] = useState("");
  const [terms, setTerms] = useState([]);
  const [paperUrl, setPaperUrl] = useState("");
  const [comment, setComment] = useState("");
  const [commentId, setCommentId] = useState("");
  const [hasComment, setHasComment] = useState(false);

  const editorRef = useRef();

  const updateComment = (updatedComment) => {
    setComment(updatedComment);
    editorRef.current.getInstance().setMarkdown(updatedComment);
  }

  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  useEffect(() => {
    UserApi.getPaper(id).then((response) => {
      console.log(response);
      setPaperName(response.title);
      setVenueType(response.venue_type);
      setVenueName(response.venue_name);
      setVenueLink(response.venue_link);
      setAuthors(response.authors);
      setAbstract(response.abstract);
      setTerms(response.keywords.split(","));
      setPaperUrl(response.paperPdf);
      if ("comment" in response) {
        updateComment(response.comment);
        setHasComment(true);
        setCommentId(response.comment_id);
      }
      
    });

    
  }, []);

  useEffect(()=>{
    try {
      AlertApi.getAlert({user: localStorage.getItem("username"), keyword:terms.join(','), paperId: id}).then(matchingPapers => {
        swal("Matching Papers Found: " + JSON.stringify(matchingPapers));
        console.log('Alert API called successfully');
      }).catch(error => {
        console.log('Error calling Alert API:', error);
      });
    } catch (error) {
      console.error('Error calling Alert API:', error);
    }
  }, [terms]);
 const addComment = async(id) => {
   
  if (hasComment) {
    CommentsApi.update(commentId, {
      paper_id: id,
      user: localStorage.getItem('username'),
      text: comment,
      keyword: terms.join(','),
    }).then(() => {
      swal('Comment updated successfully.')
    }).catch(() => {
      swal('Failed to update comment. Please try again.');
    });
  } else {
    CommentsApi.create({
      paper_id: id,
      user: localStorage.getItem('username'),
      text: comment,
      keyword: terms.join(','),
    }).then(() => {
      swal('Comment added successfully.')
    }).catch(() => {
      swal('Failed to add comment. Please try again.');
    });
  }
};
  return (
    <>
      <CustomNavbar />
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Terms</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {terms.map((term, i) => (
            <Stack key={i} direction="horizontal" gap={2} className="mb-2">
              <Form.Control
                id={`text${i}`}
                type="text"
                value={term}
                onChange={(e) => {
                    const newTerms = [...terms];
                    newTerms[i] = e.target.value;
                    setTerms(newTerms);
                }}
              ></Form.Control>
              <Button variant="outline-danger"
                onClick={() => {
                  const termsArray = [...terms];
                  const idx = termsArray.indexOf(term);
                  if (idx > -1) {
                    termsArray.splice(idx, 1);
                  }
                  setTerms(termsArray);
                }}
              >
                Delete
              </Button>
            </Stack>
          ))}
          <Button
            className="w-100"
            onClick={() => {
              const newTerms = [...terms].concat([""]);
              setTerms(newTerms);
            }}
          >
            Add Term
          </Button>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleClose}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
      <Container fluid style={{ backgroundColor: "#E8E8E8", color: "#011638" }}>
        <Row style={{ margin: "10px" }}>
          <Col style={{ maxHeight: "calc(100vh - 100px)", overflow: "scroll" }}>
            <h1 className="mt-3">{paperName}</h1>
            <Button variant="outline-secondary" style={{ float: "right" }}>
              <a style={{textDecoration: 'none', color: '#011638'}} target="_blank" href={`http://localhost:5173/graph/${id}`} rel="noreferrer">
                Visualize 🕸️
              </a>
            </Button>
            <div className="mt-3">
              <Badge bg="primary">{venueType}</Badge>
            </div>
            <h5 className="mt-3">
              <a target="blank" href={venueLink}>{venueName}</a>
            </h5>
            <h3 className="mt-3">Authors</h3>
            <p>{authors}</p>
            <h3 className="mt-3">Abstract</h3>
            <p>{abstract}</p>
            <h3 className="mt-3">
              Terms
              <Button style={{ float: "right" }} onClick={handleShow}>
                Edit
              </Button>
            </h3>
            <Stack direction="horizontal" gap={2}>
              {terms.map((term, i) => (
                <Badge key={i}>{term}</Badge>
              ))}
            </Stack>
            <h3 className="mt-3">Comments</h3>
            <Form>
              <Form.Group className="mb-3" controlId="commentsTextarea">
                <AiRewrite ref={editorRef} comment={comment} setComment={setComment} />
              </Form.Group>
              <Button variant="primary" style={{ marginRight: "10px" }} onClick={() => addComment(id)}>
                {hasComment ? "Update Comment" : "Add Comment"}
              </Button>
              <Button
                variant="primary"
               onClick={() => updateComment("")}
              >
                Clear
              </Button>
            </Form>
          </Col>
          <Col style={{ height: "calc(100vh - 100px)", margin: "10px" }}>
            <iframe src={paperUrl} width="100%" height="100%"></iframe>
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Paper;
