/* eslint-disable react/prop-types */
import { useState, useRef, useCallback } from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import ForceGraph3D from "react-force-graph-3d";
import { SizeMe } from "react-sizeme";
import { GraphApi } from "../utils/requests";

const AuthorGraph = ({ initialPaperId }) => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [authorsList, setAuthorsList] = useState([]);
  const [papersList, setPapersList] = useState([]);
  const [authorPapers, setAuthorPapers] = useState([]);
  const [modalTitle, setModalTitle] = useState("");
  const [selectedPaper, setSelectedPaper] = useState({});
  const fgRef = useRef();

  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const expandPaperAuthorsGraph = async (paperId) => {
    const paperDetails = await GraphApi.getDetails(paperId);
    const authors = paperDetails.authors.filter(
      (author) => !authorsList.includes(author.author_id)
    );
    setAuthorsList((current) => [
      ...current,
      ...authors.map((author) => author.author_id),
    ]);
    setGraphData((current) => ({
      nodes: [
        ...current.nodes,
        ...authors.map((author) => ({
          id: author.author_id,
          name: author.name,
          val: 1,
          type: "author",
        })),
      ],
      links: current.links,
    }));
    const newLinks = [];
    for (const author of paperDetails.authors) {
      if (!authorPapers.includes(`${author.author_id}-${paperId}`)) {
        newLinks.push({
          source: author.author_id,
          target: paperId,
          val: 1,
        });
        setAuthorPapers((current) => [
          ...current,
          `${author.author_id}-${paperId}`,
        ]);
      }
    }
    setGraphData((current) => ({
      nodes: current.nodes,
      links: [...current.links, ...newLinks],
    }));
    for (const author of authors) {
      const authorPapersResponse = await GraphApi.getAuthorPapers(
        author.author_id
      );
      const newNodes = [];
      const newLinks = [];
      for (const paper of authorPapersResponse) {
        if (!papersList.includes(paper.paper_id)) {
          newNodes.push({
            id: paper.paper_id,
            name: paper.title,
            val: 2,
            type: "paper",
          });
          setPapersList((current) => [...current, paper.paper_id]);
        }
        if (!authorPapers.includes(`${author.author_id}-${paper.paper_id}`)) {
          newLinks.push({
            source: author.author_id,
            target: paper.paper_id,
            val: 1,
          });
          setAuthorPapers((current) => [
            ...current,
            `${author.author_id}-${paper.paper_id}`,
          ]);
        } else {
          console.log(`${author.author_id}-${paper.paper_id} already exists`);
        }
      }
      setGraphData((current) => ({
        nodes: [...current.nodes, ...newNodes],
        links: [...current.links, ...newLinks],
      }));
    }
  };
  const instantiateGraph = async () => {
    setPapersList([]);
    setAuthorsList([]);
    setAuthorPapers([]);
    setGraphData({
      nodes: [
        {
          id: initialPaperId,
          name: "Source Paper",
          val: 200,
          type: "source",
        },
      ],
      links: [],
    });
    await expandPaperAuthorsGraph(initialPaperId);
  };

  const handleExpand = async () => {
    setShow(false);
    await expandPaperAuthorsGraph(selectedPaper);
  };

  const handleClick = useCallback(
    (node) => {
      // Aim at node from outside it
      const distance = 200;
      const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);

      fgRef.current.cameraPosition(
        { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }, // new position
        node, // lookAt ({ x, y, z })
        3000 // ms transition duration
      );
    },
    [fgRef]
  );

  const fixCameraPosition = (node, distance) => {
    const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);

    fgRef.current.cameraPosition(
      { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }, // new position
      node, // lookAt ({ x, y, z })
      2000 // ms transition duration
    );
    setTimeout(() => {
      node.fx = node.x;
      node.fy = node.y;
      node.fz = node.z;
    }, 2500);
  };

  useState(() => {
    instantiateGraph();
  }, []);

  return (
    <>
      <Modal show={show} onHide={handleClose}>
        <Modal.Body>{modalTitle}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="success" onClick={handleExpand}>
            Expand
          </Button>
          {/* <Button variant="primary" onClick={() => modalButtonAction()}>
            {modalButtonText}
          </Button> */}
        </Modal.Footer>
      </Modal>
      <SizeMe monitorHeight refreshRate={32}>
        {({ size }) => (
          <ForceGraph3D
            ref={fgRef}
            width={size.width}
            height={size.height}
            graphData={graphData}
            nodeColor={(node) => (node.type === "paper" ? "#FCBA50" : "#f8f7f7")}
            nodeAutoColorBy={(node) => node.type}
            onNodeClick={handleClick}
            onNodeRightClick={(node) => {
              console.log(node);
              if (node.type === "paper") {
                fixCameraPosition(node, 300);
                setModalTitle(node.name);
                setSelectedPaper(node.id);
                handleShow();
              }
            }}
            linkColor={() => "#FCBA50"}
            linkWidth={2}
            backgroundColor="#011638"
          />
        )}
      </SizeMe>
    </>
  );
};

export default AuthorGraph;
