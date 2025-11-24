"""
Neural Compression Metrics for Consciousness
Implementation of Theorem 5 signatures
"""

import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from scipy import stats

class NeuralCompressionAnalyzer:
    """
    Analyze neural data for consciousness-related compression signatures
    """
    
    def __init__(self, n_regions=400):
        self.n_regions = n_regions
    
    def intrinsic_dimensionality(self, neural_data):
        """
        Calculate intrinsic dimensionality (ID)
        ID = argmin_d {sum_i^d λ_i ≥ 0.95 * total_variance}
        """
        pca = PCA()
        pca.fit(neural_data)
        cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
        id_val = np.argmax(cumulative_variance >= 0.95) + 1
        return id_val
    
    def predictive_complexity(self, time_series):
        """
        Calculate predictive complexity (PC)
        PC = (1/T) * sum ||x(t) - x̂(t)||²
        """
        T = len(time_series) - 1
        errors = []
        
        for t in range(1, len(time_series)):
            # Simple linear prediction
            if t > 10:
                X_train = time_series[:t-1]
                y_train = time_series[1:t]
                model = LinearRegression()
                model.fit(X_train, y_train)
                prediction = model.predict([time_series[t-1]])
                error = np.linalg.norm(time_series[t] - prediction)
                errors.append(error)
        
        return np.mean(errors) if errors else 0
    
    def information_integration(self, connectivity_matrix):
        """
        Calculate information integration (Φ)
        Simplified version for demonstration
        """
        # Eigenvalues represent information capacity
        eigenvalues = np.linalg.eigvals(connectivity_matrix)
        real_eigs = np.real(eigenvalues)
        phi = np.sum(real_eigs[real_eigs > 0])  # Sum of positive eigenvalues
        return phi
    
    def analyze_conscious_state(self, conscious_data, unconscious_data):
        """
        Compare compression metrics between conscious and unconscious states
        """
        metrics = ['ID', 'PC', 'Phi']
        results = {}
        
        for state_name, data in [('conscious', conscious_data), 
                                ('unconscious', unconscious_data)]:
            
            if data is None:
                continue
                
            # Calculate metrics
            id_val = self.intrinsic_dimensionality(data['resting_state'])
            pc_val = self.predictive_complexity(data['time_series'])
            phi_val = self.information_integration(data['connectivity'])
            
            results[state_name] = {
                'Intrinsic_Dimensionality': id_val,
                'Predictive_Complexity': pc_val,
                'Information_Integration': phi_val
            }
        
        # Calculate effect sizes
        if 'conscious' in results and 'unconscious' in results:
            c_data = results['conscious']
            u_data = results['unconscious']
            
            effect_sizes = {}
            for metric in metrics:
                if metric == 'ID':
                    c_val, u_val = c_data['Intrinsic_Dimensionality'], u_data['Intrinsic_Dimensionality']
                elif metric == 'PC':
                    c_val, u_val = c_data['Predictive_Complexity'], u_data['Predictive_Complexity']
                else:  # Phi
                    c_val, u_val = c_data['Information_Integration'], u_data['Information_Integration']
                
                # Cohen's d
                pooled_std = np.sqrt((0.1 + 0.1) / 2)  # Simplified
                d = (c_val - u_val) / pooled_std
                effect_sizes[metric] = d
            
            results['effect_sizes'] = effect_sizes
        
        return results

# Example with synthetic data
def generate_synthetic_neural_data(n_timepoints=1000, n_regions=400, 
                                 consciousness_level='conscious'):
    """
    Generate synthetic neural data for testing
    """
    np.random.seed(42)
    
    # Different parameters for conscious vs unconscious
    if consciousness_level == 'conscious':
        # More structured, lower dimensionality
        intrinsic_dims = 18
        noise_level = 0.1
        connectivity_strength = 0.8
    else:
        # Less structured, higher dimensionality  
        intrinsic_dims = 24
        noise_level = 0.2
        connectivity_strength = 0.3
    
    # Generate low-dimensional structure
    base_patterns = np.random.randn(n_regions, intrinsic_dims)
    time_courses = np.random.randn(n_timepoints, intrinsic_dims)
    
    # Create resting state data
    resting_state = time_courses @ base_patterns.T + noise_level * np.random.randn(n_timepoints, n_regions)
    
    # Create time series with memory
    time_series = np.cumsum(np.random.randn(n_timepoints, n_regions), axis=0)
    
    # Create connectivity matrix
    connectivity = connectivity_strength * np.random.randn(n_regions, n_regions)
    connectivity = (connectivity + connectivity.T) / 2  # Symmetrize
    np.fill_diagonal(connectivity, 1.0)  # Self-connections
    
    return {
        'resting_state': resting_state,
        'time_series': time_series,
        'connectivity': connectivity
    }

if __name__ == "__main__":
    print("AEP Neural Compression Analysis")
    print("=" * 40)
    
    # Generate synthetic data
    conscious_data = generate_synthetic_neural_data(consciousness_level='conscious')
    unconscious_data = generate_synthetic_neural_data(consciousness_level='unconscious')
    
    # Analyze
    analyzer = NeuralCompressionAnalyzer()
    results = analyzer.analyze_conscious_state(conscious_data, unconscious_data)
    
    # Print results
    for state in ['conscious', 'unconscious']:
        if state in results:
            print(f"\n{state.upper()} STATE:")
            for metric, value in results[state].items():
                print(f"  {metric}: {value:.3f}")
    
    if 'effect_sizes' in results:
        print(f"\nEFFECT SIZES (Cohen's d):")
        for metric, d in results['effect_sizes'].items():
            print(f"  {metric}: d = {d:.2f}")
