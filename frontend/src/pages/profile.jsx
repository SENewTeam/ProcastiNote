import React, { useState, useEffect, useRef } from 'react';
import {
  Button,
  Col,
  Container,
  Row,
  Card,
  Modal,
  Form
} from 'react-bootstrap';
import Select from 'react-select';
import CustomNavbar from '../components/Navbar';
import AiRewrite from '../components/AiRewrite';
import { CommentsApi, UserApi } from '../utils/requests';
import './profile.css';

const Profile = () => {
  const userId    = localStorage.getItem('id');
  const username  = localStorage.getItem('username') || '';
  const firstChar = username.charAt(0);

  // multi‑select state (arrays)
  const [filters, setFilters] = useState({
    paperNames: [],
    authors:     [],
    venueTypes: [],
    years:       []
  });

  // option lists for react‑select
  const [options, setOptions] = useState({
    titles:     [],
    authors:    [],
    venueTypes: [],
    years:      []
  });

  // what we show on screen
  const [paperData,   setPaperData]   = useState([]);
  const [commentData, setCommentData] = useState([]);
  const [loading,     setLoading]     = useState(false);
  const [error,       setError]       = useState(null);

  // edit‑comment modal
  const [show, setShow] = useState(false);
  const [term, setTerm] = useState({});
  const editorRef      = useRef();

  // dedupe helper
  const uniq = arr => Array.from(new Set(arr)).sort();

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        // 1) get ALL papers for dropdowns
        const all = await UserApi.getAllPapers(userId);
        setOptions({
          titles:     uniq(all.map(p => p.title).filter(Boolean)),
          authors:    uniq(all.map(p => p.authors).filter(Boolean)),
          venueTypes: uniq(all.map(p => p.venue_type).filter(Boolean)),
          years:      uniq(all.map(p => String(p.year)).filter(Boolean))
        });

        // 2) get recent 5
        const recentRaw = await UserApi.getPapers();
        const recent = Object.entries(recentRaw)
          .slice(0, 5)
          .map(([id, [title, abstract]]) => ({
            paperId:  id,
            title,
            abstract,
            authors:  '',
            year:     '',
            venueType:'',
          }));
        setPaperData(recent);

        // 3) load comments
        setCommentData(await CommentsApi.getAllComment());
      } catch (e) {
        console.error(e);
        setError('Failed to load data');
      } finally {
        setLoading(false);
      }
    })();
  }, [userId]);

  // on multi‑select change
  const handleMultiChange = field => selected => {
    setFilters(f => ({
      ...f,
      [field]: selected ? selected.map(o => o.value) : []
    }));
  };

  // hit backend filter endpoint, passing **first** selected of each (until backend supports true multi)
  const applyFilters = async e => {
    e.preventDefault();
    const [paperName, author, venueType, year] = [
      filters.paperNames[0] || '',
      filters.authors[0]     || '',
      filters.venueTypes[0]  || '',
      filters.years[0]       || ''
    ];

    // no filters => show recent 5
    if (!paperName && !author && !venueType && !year) {
      const recentRaw = await UserApi.getPapers();
      return setPaperData(
        Object.entries(recentRaw)
          .slice(0, 5)
          .map(([id, [title, abstract]]) => ({
            paperId:  id,
            title,
            abstract,
            authors:  '',
            year:     '',
            venueType:'',
          }))
      );
    }

    setLoading(true);
    try {
      const filtered = await UserApi.filterPapers({ paperName, author, venueType, year });
      setPaperData(filtered.map(p => ({
        paperId:   p.paperId,
        title:     p.title,
        abstract:  p.abstract,
        authors:   p.authors,
        year:      p.year,
        venueType: p.venue_type
      })));
    } catch {
      setError('Failed to apply filters');
    } finally {
      setLoading(false);
    }
  };

  // comment handlers
  const handleEditComment = id => {
    const c = commentData.find(x => x._id === id);
    if (c) { setTerm(c); setShow(true); }
  };
  const updateComment = async cmt => {
    try {
      await CommentsApi.update(cmt._id, {
        user:    localStorage.getItem('username'),
        text:    cmt.text,
        keyword: cmt.keyword
      });
      setCommentData(cs => cs.map(c => c._id === cmt._id ? cmt : c));
      setShow(false);
    } catch {
      alert('Failed to update comment');
    }
  };
  const handleDeleteComment = async id => {
    try {
      await CommentsApi.deleteComment(id);
      setCommentData(cs => cs.filter(c => c._id !== id));
    } catch {
      alert('Failed to delete comment');
    }
  };

  // helper to build react‑select options
  const mkOpts = arr => arr.map(v => ({ label: v, value: v }));

  return (
    <>
      <CustomNavbar />

      {/* Edit Comment Modal */}
      <Modal show={show} onHide={() => setShow(false)}>
        <Modal.Header closeButton><Modal.Title>Edit Comment</Modal.Title></Modal.Header>
        <Modal.Body>
          <AiRewrite
            ref={editorRef}
            comment={term.text || ''}
            setComment={txt => setTerm(t => ({ ...t, text: txt }))}
          />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShow(false)}>Cancel</Button>
          <Button variant="primary"   onClick={() => updateComment(term)}>Save</Button>
        </Modal.Footer>
      </Modal>

      <Container fluid className="dashboard-container">

        {/* Profile Header */}
        <Row className="align-items-center mb-4">
          <Col xs="auto">
            <div className="profile-circle">{firstChar}</div>
          </Col>
          <Col>
            <h2 className="profile-username">Hi {username}</h2>
          </Col>
        </Row>

        {/* Multi‑Select Filter Bar */}
        <Container fluid className="filter-section">
          <Row className="gx-2 align-items-center">
            <Col md={3}>
              <Select
                isMulti
                placeholder="Paper Name…"
                options={mkOpts(options.titles)}
                value={mkOpts(options.titles).filter(o => filters.paperNames.includes(o.value))}
                onChange={handleMultiChange('paperNames')}
                className="react-select-container"
                classNamePrefix="react-select"
              />
            </Col>
            <Col md={3}>
              <Select
                isMulti
                placeholder="Authors…"
                options={mkOpts(options.authors)}
                value={mkOpts(options.authors).filter(o => filters.authors.includes(o.value))}
                onChange={handleMultiChange('authors')}
                className="react-select-container"
                classNamePrefix="react-select"
              />
            </Col>
            <Col md={3}>
              <Select
                isMulti
                placeholder="Venue Type…"
                options={mkOpts(options.venueTypes)}
                value={mkOpts(options.venueTypes).filter(o => filters.venueTypes.includes(o.value))}
                onChange={handleMultiChange('venueTypes')}
                className="react-select-container"
                classNamePrefix="react-select"
              />
            </Col>
            <Col md={2}>
              <Select
                isMulti
                placeholder="Years…"
                options={mkOpts(options.years)}
                value={mkOpts(options.years).filter(o => filters.years.includes(o.value))}
                onChange={handleMultiChange('years')}
                className="react-select-container"
                classNamePrefix="react-select"
              />
            </Col>
            <Col md={1} className="text-end">
              <Button onClick={applyFilters}>Apply</Button>
            </Col>
          </Row>
        </Container>

        {/* ——— Recently read by you ——— */}
        <Container fluid className="mb-5">
          <h2 style={{ margin: '20px' }}>Recently read by you:</h2>
          {loading && <p>Loading…</p>}
          {error   && <p className="text-danger">{error}</p>}
          {!loading && paperData.length === 0 && <p>No papers found.</p>}
          <Row className="mx-2">
            {paperData.map(c => (
              <Col key={c.paperId} sm={12} md={6} lg={3} xxl={2}>
                <Card style={{ height: '100%' }}>
                  <Card.Body style={{ display: 'flex', flexDirection: 'column' }}>
                    <Card.Title>{c.title}</Card.Title>
                    <Card.Text className="card-description" style={{ flexGrow: 1 }}>
                      {c.abstract}
                    </Card.Text>
                    <Card.Link href={`/paper/${c.paperId}`}>
                      Continue Reading…
                    </Card.Link>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Container>

        {/* ——— Comments ——— */}
        <Container fluid className="mb-5">
          <h2 style={{ margin: '20px' }}>Comments:</h2>
          <Row className="mx-2 mb-3">
            {commentData.map(c => (
              <Col key={c._id} sm={12} md={6} lg={3} xxl={2}>
                <Card style={{ height: '100%' }}>
                  <Card.Body style={{ display: 'flex', flexDirection: 'column' }}>
                    <Card.Title>{c.paperTitle}</Card.Title>
                    <Card.Text className="flex-grow-1">{c.text}</Card.Text>
                    <div className="d-flex justify-content-between">
                      <Button size="sm" onClick={() => handleEditComment(c._id)}>
                        Edit
                      </Button>
                      <Button
                        size="sm"
                        variant="danger"
                        onClick={() => handleDeleteComment(c._id)}
                      >
                        Delete
                      </Button>
                    </div>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </Container>

      </Container>
    </>
  );
};

export default Profile;
