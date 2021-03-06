package com.example.backend.config;

import java.util.ArrayList;
import java.util.List;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;

import lombok.Data;

@Data
@EnableAsync
@Configuration
@ConfigurationProperties(prefix = "app")
public class AppConfig {
    public List<String> getAuthorizedRedirectUris() {
        return authorizedRedirectUris;
    }

    private List<String> authorizedRedirectUris = new ArrayList<>();

    public String getTokenSecret() {
        return tokenSecret;
    }

    public long getTokenExpirationMsec() {
        return tokenExpirationMsec;
    }

    private String tokenSecret = "XhKJipRfDRN4QE3s0LVlAffxgH46keJK3U7PQCxWXM4pbGDROUCPPB8udKCuX7q";

    private long tokenExpirationMsec = 1860000;

}
