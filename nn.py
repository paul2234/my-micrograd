from mymicrograd.engine import Value
import random

class Module:
    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0

    def parameters(self):
        return []
    
class Neuron(Module):
    def __init__(self,nin: int,nonlin = True):
        self.w = [Value(random.uniform(-1,1)) for _ in range(nin)]
        self.b = Value(0.0)
        self.nonlin = nonlin

    def __call__(self,x: list):
        assert len(self.w) == len(x),f"len(self.w) is {len(self.w)} and len(x) is {len(x)}"

        act = sum((a * b for a,b in zip(self.w,x)),self.b)
        return act.relu() if self.nonlin else act
    
    def parameters(self):
        return self.w + [self.b]
    
class Layer(Module):
    def __init__(self,nin,nout,**kwargs):
        self.neurons = [Neuron(nin,**kwargs) for _ in range(nout)]

    def __call__(self,x):
        out = [n(x) for n in self.neurons]
        return out[0] if len(out) == 1 else out
    
    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]
    
class MLP(Module):
    def __init__(self,nin,nouts):
        size = [nin] + nouts
        self.layers = [Layer(size[i],size[i + 1],nonlin=i!=len(nouts) - 1) for i in range(len(nouts))]

    def __call__(self,x):
        for layer in self.layers:
            x = layer(x)
        return x
    
    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]
