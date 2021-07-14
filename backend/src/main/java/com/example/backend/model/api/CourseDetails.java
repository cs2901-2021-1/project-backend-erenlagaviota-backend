package com.example.backend.model.api;

public class CourseDetails {
    public String getCodcurso() {
        return codcurso;
    }

    public void setCodcurso(String codcurso) {
        this.codcurso = codcurso;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    private String codcurso;
    private String department;
    private String name;
}
