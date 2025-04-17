/* eslint-disable react/prop-types */
import { useState, useRef, useCallback } from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import ForceGraph3D from "react-force-graph-3d";
import { SizeMe } from "react-sizeme";
import { GraphApi } from "../utils/requests";

const ReferencesGraph = ({ initialPaperId }) => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [papersList, setPapersList] = useState([]);
  const [paperReferencesList, setPaperReferencesList] = useState([]);
  const [modalTitle, setModalTitle] = useState("");
  const [selectedPaper, setSelectedPaper] = useState({});
  const fgRef = useRef();

  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const expandPaperReferencesGraph = async (paperId) => {
    const references = await GraphApi.getReferences(paperId);
    const paperReferences = references.filter(
      (reference) => !papersList.includes(reference.paper_id)
    );
    setGraphData((current) => ({
      nodes: [
        ...current.nodes,
        ...paperReferences.map((reference) => ({
          id: reference.paper_id,
          name: reference.title,
          val: 1,
          type: "paper",
        })),
      ],
      links: current.links,
    }));
    const newLinks = [];
    for (const reference of paperReferences) {
      if (!paperReferencesList.includes(`${paperId}-${reference.paper_id}`)) {
        newLinks.push({
          source: paperId,
          target: reference.paper_id,
          val: 1,
        });
        setPaperReferencesList((current) => [
          ...current,
          `${paperId}-${reference.paper_id}`,
        ]);
      }
    }
    setGraphData((current) => ({
      nodes: current.nodes,
      links: [...current.links, ...newLinks],
    }));
  };
  const instantiateGraph = async () => {
    setPapersList([]);
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
    await expandPaperReferencesGraph(initialPaperId);
  };

  const handleExpand = async () => {
    setShow(false);
    await expandPaperReferencesGraph(selectedPaper);
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
        </Modal.Footer>
      </Modal>
      <SizeMe monitorHeight refreshRate={32}>
        {({ size }) => (
          <ForceGraph3D
            ref={fgRef}
            width={size.width}
            height={size.height}
            graphData={graphData}
            nodeColor={(node) => (node.type === "paper" ? "#00f" : "#f00")}
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
            linkColor={() => "#000"}
            backgroundColor="#fff"
          />
        )}
      </SizeMe>
    </>
  );
};

export default ReferencesGraph;
