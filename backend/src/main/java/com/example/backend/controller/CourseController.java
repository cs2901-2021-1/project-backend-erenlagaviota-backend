package com.example.backend.controller;

import java.util.HashMap;

import com.example.backend.config.Constants;
import com.nimbusds.jose.shaded.json.JSONArray;

import org.hibernate.mapping.Map;
import org.springframework.http.client.support.BasicAuthenticationInterceptor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import lombok.RequiredArgsConstructor;

// @RestController
// @RequiredArgsConstructor
// @RequestMapping("/courses")
// public class CourseController {
//     @GetMapping("/valid")
//     @PreAuthorize("hasRole('USER')")
//     public Object getValidCourses() {
//             // var restTemplate = new RestTemplate();
//             // restTemplate.getInterceptors().add(new BasicAuthenticationInterceptor("prueba", "prueba"));
//             // JSONArray response = new JSONArray();
//             HashMap<String,String> error = new HashMap<>();
//             return error;
//         // try {
//         //     var restTemplate = new RestTemplate();
//         //     restTemplate.getInterceptors().add(new BasicAuthenticationInterceptor("prueba", "prueba"));
//         //     JSONArray response = new JSONArray();
//         //     response = restTemplate.getForObject(Constants.ENDPOINT_URL + "api/cursos/valid", response.getClass());
//         //     return response;
//         // } catch (Exception e) {
//         //     HashMap<String,String> error = new HashMap<>();
//         //     error.put("error",e.getMessage());
//         //     return error;
//         // }
//     }
// }
//
@RestController
@RequiredArgsConstructor
public class CourseController {
    @GetMapping("/courses")
    @PreAuthorize("hasRole('USER')")
    public HashMap<String,String> getCurrentUser(){
        HashMap<String,String> error = new HashMap<>();
        error.put("asdd","asdd");
        return error;
    }
}
