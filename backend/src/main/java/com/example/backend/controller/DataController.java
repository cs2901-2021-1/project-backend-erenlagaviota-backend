package com.example.backend.controller;


import com.example.backend.model.CourseDTO;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;


@RestController
@RequiredArgsConstructor
public class DataController {

    @PostMapping("/data")
    @PreAuthorize("hasRole('USER')")
    public Map<String, String> getData(@RequestBody CourseDTO courseDTO) {
        HashMap<String, String> course = new HashMap<>();
        course.put("course",courseDTO.getName());

        HttpEntity<HashMap<String, String>> request = new HttpEntity<>(course);

        var restTemplate = new RestTemplate();
        restTemplate.getInterceptors().add(new BasicAuthorizationInterceptor("prueba", "prueba"));
        String response = restTemplate.postForObject("http://3.143.255.114/api/numerical/data", request, String.class);

        HashMap<String, String> result = new HashMap<>();
        result.put("response", response);
        return result;
    }
}
