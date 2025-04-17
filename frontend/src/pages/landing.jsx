import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Image from 'react-bootstrap/Image';
import './landing.css';
import Card from 'react-bootstrap/Card';
import landingImage from '../images/landing.jpeg';


const Landing = () => {
    const navigate = useNavigate();
    const handleRegisterClick = () => {
        navigate('/register');
      };
    return (
        <div className="landing-container">
            <Container className="main-content">
                <Row className="info">
                <Col xs={12} lg={6}>
                <div className="info-text">
                            <h2 style={{ justifyContent: "center" }}>Researcher’s Hive</h2>
                            <Row xs={2} md={4} lg={6} fluid="false" className="justify-content-middle">Researcher's Hive is a powerful research tool that helps you manage your research knowledge. With its intuitive interface and comprehensive features, we make it easy for you to find and organize research papers, capture your ideas and insights and get personalized recommendations.
                            </Row>
                            <br></br>
                            <br></br>
                            <Button type="submit">Know More</Button>
                        </div>
                    </Col>
                    <Col xs={12} lg={6}>
                        <div className="info-image">
                        <Image
                            src={landingImage}
                            alt="Empty placeholder"
                            width={400}
                            height={300}
                            thumbnail
                        />
                        </div>
                    </Col>
                </Row>
            </Container>
            <br></br>
            <Container>
                <h2 className="center"> Benefits</h2>
                <div style={{ display: 'flex', marginTop: '2%' }}>
                    <Card style={{ width: '22rem', marginLeft: '2%' }}>
                        <Card.Body>
                            <Card.Title>New ways to Add Comments</Card.Title>
                            <Card.Text>
                            Elevate your research experience with our powerful commenting system. Go beyond simple text annotations and add visual elements like images and tables to enhance your understanding and communication. 
                            </Card.Text>
                        </Card.Body>
                    </Card>
                    <Card style={{ width: '22rem', marginLeft: '5%' }}>
                        <Card.Body>
                            <Card.Title>Organize Your Research</Card.Title>
                            <Card.Text>
                            Store your papers, notes, and ideas in a way that makes sense to you. Researcher's Hive's flexible tagging system that alerts you when you view similar papers. This keeps you looking for more!
                            </Card.Text>
                        </Card.Body>
                    </Card>
                    <Card style={{ width: '22rem', marginLeft: '5%' }}>
                        <Card.Body>
                            <Card.Title>Visualize Your Data</Card.Title>
                            <Card.Text>
                            See your research data in a whole new light with Researcher's Hive's interactive visualizations. Explore connections between papers, authors, track citations, and see the big picture of your research.
                            </Card.Text>
                        </Card.Body>
                    </Card>
                    <Card style={{ width: '22rem', marginLeft: '5%' }}>
                        <Card.Body>
                            <Card.Title> Get Personalized Recommendations</Card.Title>
                            <Card.Text>
                            Our recommendation system learns from your research habits and interests to suggest papers that you're likely to find relevant and useful. 
                            </Card.Text>
                        </Card.Body>
                    </Card>
                </div>
            </Container>
            <div className="center-div">
        <Button variant="primary" onClick={handleRegisterClick}>Register</Button>
      </div>
        </div>
    );
};

export default Landing;