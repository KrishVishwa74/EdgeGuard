#include <iostream>
#include <vector>
#include <onnxruntime_cxx_api.h>
#include <string>
#include <unistd.h>  // for getcwd

int main() {
    std::cout << "🚀 Initializing Edge-Guard C++ Inference Engine..." << std::endl;

    // Get working directory
    char cwd[512];
    if (getcwd(cwd, sizeof(cwd)) == nullptr) {
        std::cerr << "❌ Failed to get working directory" << std::endl;
        return 1;
    }

    std::cout << "Current working directory: " << cwd << std::endl;

    // Model path
    std::string model_path_str = std::string(cwd) + "/models/anomaly_model.onnx";
    std::cout << "Loading model from: " << model_path_str << std::endl;

    try {
        Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "EdgeGuard");
        Ort::SessionOptions session_options;
        session_options.SetIntraOpNumThreads(1);

        Ort::Session session(env, model_path_str.c_str(), session_options);

        std::cout << "✅ Model loaded successfully!" << std::endl;

        // Simulated live data
        std::vector<std::vector<float>> live_data_stream = {
            {12.5f, 3.8f, 0.0f},
            {16.1f, 4.2f, 1.0f},
            {195.0f, 28.5f, 14.0f},  // anomaly
            {14.0f, 3.9f, 0.0f}
        };

        std::vector<int64_t> input_shape = {1, 3};
        auto memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);

        const char* input_names[] = {"float_input"};
        const char* output_names[] = {"label"};

        std::cout << "\n--- Monitoring Started ---" << std::endl;

        for (size_t i = 0; i < live_data_stream.size(); ++i) {
            auto& current = live_data_stream[i];

            Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
                memory_info, current.data(), current.size(),
                input_shape.data(), input_shape.size()
            );

            auto output_tensors = session.Run(
                Ort::RunOptions{nullptr},
                input_names, &input_tensor, 1,
                output_names, 1
            );

            const int64_t* output = output_tensors[0].GetTensorData<int64_t>();

            std::cout << "[Event " << i + 1 << "] ";

            if (output[0] == -1) {
                std::cout << "❌ ANOMALY DETECTED\n";

                // Extract values
                int frequency = static_cast<int>(current[0]);
                int payload_size = static_cast<int>(current[1]);
                int failed_logins = static_cast<int>(current[2]);

                // Build curl command
                std::string cmd =
                "curl -X POST http://127.0.0.1:8000/alert "
                "-H \"Content-Type: application/json\" "
                "-d \"{\\\"event_id\\\":" + std::to_string(i + 1) +
                ",\\\"frequency\\\":" + std::to_string(frequency) +
                ",\\\"payload_size\\\":" + std::to_string(payload_size) +
                ",\\\"failed_logins\\\":" + std::to_string(failed_logins) +
                "}\"";
                std::cout << "Sending JSON: " << cmd << std::endl;

                system(cmd.c_str());
            }
            else {
                std::cout << "🟢 NORMAL\n";
            }
        }

    } catch (const std::exception& e) {
        std::cerr << "❌ ERROR: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}