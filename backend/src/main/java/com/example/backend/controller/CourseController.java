package com.example.backend.controller;


import com.example.backend.config.Constants;
import com.nimbusds.jose.shaded.json.JSONArray;

import org.springframework.http.client.support.BasicAuthenticationInterceptor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;


import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
@RequestMapping("/courses")
public class CourseController {
    @GetMapping("/valid")
    @PreAuthorize("hasRole('USER')")
    public JSONArray getValidCourses(){
        var restTemplate = new RestTemplate();
        restTemplate.getInterceptors().add(new BasicAuthenticationInterceptor("prueba", "prueba"));
        JSONArray response = new JSONArray();
        response = restTemplate.getForObject(Constants.ENDPOINT_URL + "api/cursos/valid", response.getClass());
        return response;
    }
}
