import { spawn } from 'child_process';
import path from 'path';

/**
 * @param {Function} onTranscript 
 */
export function startVoiceTranscription(onTranscript) {
    const scriptPath = path.join(process.cwd(), 'utils', 'voice', 'voiceTranscription.py');
    const pythonProcess = spawn('python3', [scriptPath]);

    console.log("🎙️ Voice System Initialized. Use CAPS LOCK to record.");

    pythonProcess.stdout.on('data', (data) => {
        const transcript = data.toString().trim();
        if (transcript) {
            onTranscript(transcript);
        }
    });

    // pythonProcess.stderr.on('data', (data) => {
    //     const status = data.toString().trim();
    //     console.log(`[PYTHON]: ${status}`);
    // });

    pythonProcess.on('error', (err) => {
        console.error('CRITICAL: Failed to start Python voice script:', err);
    });

    return pythonProcess;
}