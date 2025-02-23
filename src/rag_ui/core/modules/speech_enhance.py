import numpy as np
from scipy.signal import stft, istft
from scipy.io import wavfile

def spectral_subtraction(noisy_signal, sr, noise_frames=10, alpha=1.0, beta=0.02, nperseg=1024):
    """
    Perform spectral subtraction on a noisy signal using SciPy.

    Parameters:
        noisy_signal (np.array): The input noisy audio signal.
        sr (int): Sampling rate.
        noise_frames (int): Number of initial STFT frames assumed to contain mostly noise.
        alpha (float): Over-subtraction factor.
        beta (float): Spectral floor factor.
        nperseg (int): Number of samples per segment in STFT.

    Returns:
        clean_signal (np.array): The enhanced time-domain audio signal.
    """
    # Compute the STFT of the noisy signal
    f, t, Zxx = stft(noisy_signal, fs=sr, nperseg=nperseg)
    magnitude = np.abs(Zxx)
    phase = np.angle(Zxx)
    print("Zxx shape: ", Zxx.shape)

    # Estimate the noise magnitude spectrum from the first few frames
    noise_est = np.mean(magnitude[:, :noise_frames], axis=1, keepdims=True)

    # Subtract the estimated noise spectrum (with over-subtraction)
    subtracted_mag = magnitude - alpha * noise_est

    # Apply spectral flooring to prevent negative or too-small values
    subtracted_mag = np.where(subtracted_mag < beta * noise_est, beta * noise_est, subtracted_mag)

    # Reconstruct the STFT with the original phase
    Zxx_clean = subtracted_mag * np.exp(1j * phase)

    # Compute the inverse STFT to get the time-domain signal
    _, clean_signal = istft(Zxx_clean, fs=sr, nperseg=nperseg)

    return clean_signal

import numpy as np
from scipy.io import wavfile

def kalman_filter_audio(input_path, output_path, Q=0.01, R=0.1):
    """
    Apply Kalman filtering to denoise a speech audio file.
    
    Parameters:
    - input_path: Path to the input noisy audio file.
    - output_path: Path to save the filtered audio.
    - F: State transition coefficient (default: 1).
    - Q: Process noise covariance (default: 0.01).
    - R: Measurement noise covariance (default: 0.1).
    - normalize: Normalize output to prevent clipping (default: True).
    """
    # Load audio file
    sr, y = wavfile.read(input_path)
    
    # Ensure y is in float format for processing
    if y.dtype != np.float32 and y.dtype != np.float64:
        y = y.astype(np.float32) / np.iinfo(y.dtype).max
    
    # Initialize Kalman filter variables
    n_samples = len(y)
    x_est = np.zeros(n_samples)
    x_est[0] = y[0]
    P = np.var(y)  # Initial error covariance
    
    # Kalman filter loop
    for i in range(1, n_samples):
        # Prediction step
        x_pred = x_est[i-1]
        P_pred = P + Q
        
        # Update step
        y_residual = y[i] - x_pred
        S = P_pred + R
        K = P_pred / S  # Kalman gain
        
        x_est[i] = x_pred + K * y_residual
        P = (1 - K) * P_pred
    
    # Convert back to 16-bit PCM format
    x_est_int16 = (x_est * np.iinfo(np.int16).max).astype(np.int16)
    
    # Save filtered audio
    wavfile.write(output_path, sr, x_est_int16)

if __name__ == '__main__':
    # # Read the noisy audio file (ensure it's a WAV file)
    # sr, noisy_signal = wavfile.read('src/rag_ui/data/audio/noisy_speech.wav')

    # # If the audio is stereo, convert to mono by averaging the channels
    # if noisy_signal.ndim > 1:
    #     noisy_signal = np.mean(noisy_signal, axis=1)

    # # If the audio data is in integer format, convert it to float in the range [-1, 1]
    # if noisy_signal.dtype.kind in 'iu':
    #     max_val = np.iinfo(noisy_signal.dtype).max
    #     noisy_signal = noisy_signal.astype(np.float32) / max_val

    # # Apply spectral subtraction
    # clean_signal = spectral_subtraction(noisy_signal, sr)

    # # Optionally, scale the clean signal back to int16 for saving as a WAV file
    # clean_signal_int16 = np.int16(clean_signal / np.max(np.abs(clean_signal)) * 32767)
    # wavfile.write('src/rag_ui/data/audio/enhanced_audio.wav', sr, clean_signal_int16)

    kalman_filter_audio('src/rag_ui/data/audio/noisy_speech.wav', 'src/rag_ui/data/audio/kalman.wav')
    kalman_filter_audio('src/rag_ui/data/audio/kalman.wav', 'src/rag_ui/data/audio/kalman2.wav')
    # kalman_filter_audio('src/rag_ui/data/audio/kalman2.wav', 'src/rag_ui/data/audio/kalman3.wav')
