package com.example.backend;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.parallel.Execution;
import org.junit.jupiter.api.parallel.ExecutionMode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.web.server.LocalServerPort;

import static org.assertj.core.api.Assertions.assertThat;

import com.example.backend.config.Constants;
import com.example.backend.model.api.ResponseCourseNumericalProjection;
import com.nimbusds.jose.shaded.json.JSONArray;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.client.support.BasicAuthenticationInterceptor;
import org.springframework.web.client.RestTemplate;

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@Execution(ExecutionMode.CONCURRENT)
class BackendApplicationTests {

    @LocalServerPort
    private int port;

    @Autowired
    private TestRestTemplate restTemplate;

    private static final String authToken = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI5OSIsImlhdCI6MTYyNzYzMzg4MiwiZXhwIjoxNjI3NjM1NzQyfQ.bhPShHY-K3eg8Psa3viV7TQjkSkLdLSDXHcrb8rUbp8OOrPdmPKUKvfBe_o-oHaOJxpdnnOyfPLjeU6eKrmxyA";

    @Test
    void contextLoads() {
        assertThat(port).isNotZero();
    }

    @Test
    void test1() {
        String url = "http://localhost:" + port + "/courses/valid/";
        assertThat(restTemplate.getForEntity(url, String.class).getStatusCodeValue()).isEqualTo(401);
    }

    @Test
    void test2() {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer " + authToken);
        String url = "http://localhost:" + port + "/courses/valid/";
        assertThat(restTemplate.exchange(url, HttpMethod.GET, new HttpEntity<>(headers), String.class)
                .getStatusCodeValue()).isEqualTo(200);
    }

    @Test
    void test3() {
        String url = "http://localhost:" + port + "/profile/";
        assertThat(restTemplate.getForEntity(url, String.class).getStatusCodeValue()).isEqualTo(401);
    }

    @Test
    void test4() {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer " + authToken);
        String url = "http://localhost:" + port + "/profile/";
        assertThat(restTemplate.exchange(url, HttpMethod.GET, new HttpEntity<>(headers), String.class)
                .getStatusCodeValue()).isEqualTo(200);
    }

    @Test
    void test5() {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer " + authToken);
        String url = "http://localhost:" + port + "/data/numericalProjection/";
        var course = new ResponseCourseNumericalProjection();
        course.setCourse("AAAAAA");

        HttpEntity<ResponseCourseNumericalProjection> requestEntity = new HttpEntity<>(course, headers);

        assertThat(restTemplate.exchange(url, HttpMethod.POST, requestEntity, String.class).getStatusCodeValue())
                .isEqualTo(500);
    }

    @Test
    void test6() {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer " + authToken);
        String url = "http://localhost:" + port + "/data/numericalProjection/";
        var course = new ResponseCourseNumericalProjection();
        course.setCourse("CS2S01");

        HttpEntity<ResponseCourseNumericalProjection> requestEntity = new HttpEntity<>(course, headers);

        assertThat(restTemplate.exchange(url, HttpMethod.POST, requestEntity, String.class).getStatusCodeValue())
                .isEqualTo(200);
    }
}
