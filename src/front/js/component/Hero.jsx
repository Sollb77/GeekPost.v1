import React from "react";
import "../../styles/index.css";
import YouTube from "react-youtube";

export const Hero = () => (
    <section id="hero" className="d-flex align-items-center p-3">
        <div className="container">
            <div className="row">
                <div
                    className="col-lg-6 d-flex flex-column justify-content-center pt-4 pt-lg-0 mt-md-5 pt-md-5"
                    data-aos="fade-up"
                    data-aos-delay="200"
                >
                    <h1 className="hero-h1">
                        Publica en redes sociales de una manera sencilla...
                    </h1>
                    <h2 className="fs-1">... muy sencilla.</h2>
                    <div className="d-flex justify-content-center justify-content-lg-start">
                        <a href="#about" className="btn-get-started">
                            Regístrate 🖋
                        </a>
                        <a
                            href="#"
                            className="glightbox btn-watch-video nav-link"
                        >
                            <span>&gt; Watch Video 🎥</span>
                        </a>
                    </div>
                </div>
                <div
                    className="col-lg-6 hero-img"
                    data-aos="zoom-in"
                    data-aos-delay="200"
                >
                    <div className="embed-responsive embed-responsive-16by9 mt-5">
                        <YouTube
                            className="embed-responsive-item d-flex justify-content-center w-100 mt-md-5"
                            controls
                            autoPlay
                            muted
                            videoId="jgm58cbu0kw"
                        />
                    </div>
                </div>
            </div>
        </div>
    </section>
);
