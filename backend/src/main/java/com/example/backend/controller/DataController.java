package com.example.backend.controller;


import com.example.backend.config.Constants;
import com.example.backend.model.api.ResponseCourseNumericalProjection;
import com.example.backend.model.api.CourseNumericalProjection;

import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpEntity;
import org.springframework.http.client.support.BasicAuthenticationInterceptor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;


@RestController("/data")
@RequiredArgsConstructor
public class DataController {

    @PostMapping("/numericalProjection")
    @PreAuthorize("hasRole('USER')")
    public Map<String, Integer> getNumericalProjection(@RequestBody ResponseCourseNumericalProjection courseDTO) {
        HashMap<String, String> course = new HashMap<>();
        course.put("course",courseDTO.getCourse());

        HttpEntity<HashMap<String, String>> request = new HttpEntity<>(course);

        var restTemplate = new RestTemplate();
        restTemplate.getInterceptors().add(new BasicAuthenticationInterceptor("prueba", "prueba"));
        var response = restTemplate.postForObject(Constants.ENDPOINT_URL + "api/numerical/data", request, CourseNumericalProjection.class);

        HashMap<String, Integer> result = new HashMap<>();
        result.put("numericalProjection", response.getNumericalProjection());
        return result;
    }
}
