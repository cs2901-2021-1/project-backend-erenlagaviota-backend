package com.example.backend.model.api;

public class ResponseCourseNumericalProjection {
    private String course;
    private String onDemand;

    public String getCourse() {
        return course;
    }

    public void setCourse(String name) {
        this.course = name;
    }

    public String getOnDemand() {
        return onDemand;
    }

    public void setOnDemand(String onDemand) {
        this.onDemand = onDemand;
    }
}
