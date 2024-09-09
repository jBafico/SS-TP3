package org.example;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.text.SimpleDateFormat;

import java.io.FileWriter;
import java.io.IOException;
import java.util.Date;
import java.util.Optional;

public class Main {
    public static void main(String[] args) {
        System.out.println("Starting simulation!");

        // todo replace with json parameters
        int numberOfParticles = 30;
        double wallRadius = 100;
        double particleRadius = 1;
        double obstacleRadius = 3;
        double velocityModulus = 1;
        double particleMass = 1;
        Optional<Double> obstacleMass = Optional.empty();
        int maxEvents = 500;

        // Get the current timestamp
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());

        // Generate output json file name that has current timestamp
        String filenameWithTimestamp = "simulation_" + timeStamp + ".json";

        try (FileWriter writer = initializeOutputJson(filenameWithTimestamp)){
            MDSimulation simulation = new MDSimulation(numberOfParticles, wallRadius, particleRadius, obstacleRadius, velocityModulus, particleMass, obstacleMass, maxEvents);
            simulation.start(writer);
            writer.write("\n]\n}");
        }catch (IOException e){
            throw new RuntimeException(e);
        }


    }

    //TODO add params
    private static FileWriter initializeOutputJson(String outputJsonName) throws IOException {
        FileWriter writer = new FileWriter("./files/%s".formatted(outputJsonName));
        writer.write("{\n\"global_params\": ");
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        //gson.toJson(global_params, writer);
        writer.write(",\n");
        writer.write("\"simulations\": [\n");
        return writer;
    }
}