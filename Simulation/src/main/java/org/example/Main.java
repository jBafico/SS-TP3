package org.example;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.InputStream;
import java.text.SimpleDateFormat;

import java.io.FileWriter;
import java.io.IOException;
import java.util.Date;
import java.util.Optional;

public class Main {
    public static void main(String[] args) {
        System.out.println("Starting simulation!");

        Params params = null;
        try {
            // Load the JSON file from resources
            InputStream inputStream = Main.class.getClassLoader().getResourceAsStream("./globalParams.json");

            // Create an ObjectMapper instance
            ObjectMapper objectMapper = new ObjectMapper();

            // Read the JSON and map it to the Params class
            params = objectMapper.readValue(inputStream, Params.class);
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }


        // Get the current timestamp
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());

        // Generate output json file name that has current timestamp
        String filenameWithTimestamp = "simulation_" + timeStamp + ".json";

        if (!params.isRunMultipleTimes()){
            try (FileWriter writer = initializeOutputJson(filenameWithTimestamp, params)) {
                MDSimulation simulation = new MDSimulation(params.getNumberOfParticles(), params.getWallRadius(), params.getParticleRadius(), params.getObstacleRadius(), params.getVelocityModulus(), params.getParticleMass(), Optional.ofNullable(params.getObstacleMass()), params.getMaxEvents());
                simulation.start(writer);
                writer.write("\n]\n}");
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            return;
        }
        try (FileWriter writer = initializeOutputJsonForMultipleVelocity(filenameWithTimestamp, params)) {
            writer.write("[");
            var velocityArray = params.getVelocityModulusArray();

            for (int it = 0 ; it < velocityArray.length; it++){
                double velocity = velocityArray[it];
                writer.write("{\n\"global_params\": ");
                Gson gson = new GsonBuilder().setPrettyPrinting().create();
                params.setVelocityModulus(velocity);
                gson.toJson(params, writer);
                writer.write(",\n");
                writer.write("\"simulations\": [\n");
                for (int i = 1; i <= params.getRerunQty(); i++){
                    writer.write("{ \"simulation_%d\" : [ ".formatted(i));
                    MDSimulation simulation = new MDSimulation(params.getNumberOfParticles(), params.getWallRadius(), params.getParticleRadius(), params.getObstacleRadius(), params.getVelocityModulus(), params.getParticleMass(), Optional.ofNullable(params.getObstacleMass()), params.getMaxEvents());
                    simulation.start(writer);
                    if (i != params.getRerunQty()){
                        writer.write("]},");
                    } else {
                        writer.write("]}");
                    }
                }
                writer.write("\n]\n}");
                if (it != velocityArray.length - 1){
                    writer.write(",");
                }
            }
            writer.write("]");


        } catch (IOException e) {
            throw new RuntimeException(e);
        }




    }

    private static FileWriter initializeOutputJsonForMultipleVelocity(String outputJsonName,Params params) throws IOException {
        return new FileWriter("./files/%s".formatted(outputJsonName));
    }

    //TODO add params
    private static FileWriter initializeOutputJson(String outputJsonName,Params params) throws IOException {
        FileWriter writer = new FileWriter("./files/%s".formatted(outputJsonName));
        writer.write("{\n\"global_params\": ");
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        gson.toJson(params, writer);
        writer.write(",\n");
        writer.write("\"simulations\": [\n");
        return writer;
    }
}