# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/01_mcmc.ipynb.

# %% auto 0
__all__ = ['time2str', 'timeit', 'histogram', 'Normal', 'init_Normal', 'Uniform', 'init_Uniform', 'Exponential',
           'init_Exponential', 'StudentT', 'init_StudentT', 'HalfNormal', 'init_HalfNormal', 'Jeffreys',
           'init_Jeffreys', 'Parameter', 'StatsModel']

# %% ../notebooks/01_mcmc.ipynb 2
from fastcore.utils import patch

# %% ../notebooks/01_mcmc.ipynb 3
from pylab import *
import emcee
import warnings
from scipy.special import gammaln,gamma

# %% ../notebooks/01_mcmc.ipynb 4
import time

def time2str(tm):
    
    frac=tm-int(tm)
    tm=int(tm)
    
    s=''
    sc=tm % 60
    tm=tm//60
    
    mn=tm % 60
    tm=tm//60
    
    hr=tm % 24
    tm=tm//24
    dy=tm

    if (dy>0):
        s=s+"%d d, " % dy

    if (hr>0):
        s=s+"%d h, " % hr

    if (mn>0):
        s=s+"%d m, " % mn


    s=s+"%.2f s" % (sc+frac)

    return s

def timeit(reset=False):
    global _timeit_data
    try:
        _timeit_data
    except NameError:
        _timeit_data=time.time()

    if reset:
        _timeit_data=time.time()

    else:
        return time2str(time.time()-_timeit_data)


# %% ../notebooks/01_mcmc.ipynb 5
def histogram(y,bins=50,plot=True):
    N,bins=np.histogram(y,bins)
    
    dx=bins[1]-bins[0]
    if dx==0.0:  #  all in 1 bin!
        val=bins[0]
        bins=np.linspace(val-abs(val),val+abs(val),50)
        N,bins=np.histogram(y,bins)
    
    dx=bins[1]-bins[0]
    x=bins[0:-1]+(bins[1]-bins[0])/2.0
    
    y=N*1.0/np.sum(N)/dx
    
    if plot:
        py.plot(x,y,'o-')
        yl=py.gca().get_ylim()
        py.gca().set_ylim([0,yl[1]])
        xl=py.gca().get_xlim()
        if xl[0]<=0 and xl[0]>=0:    
            py.plot([0,0],[0,yl[1]],'k--')

    return x,y


# %% ../notebooks/01_mcmc.ipynb 7
from scipy.stats import distributions as D

def Normal(μ,σ,sum=True):
    
    def _Normal(x):
        try:
            N=len(x)
        except TypeError:
            N=1
            
        values=-0.5*np.log(2*np.pi*σ**2) - (x-μ)**2/σ**2/2.0
        
        if sum:
            return np.sum(values)
        else:
            return values
        
    return _Normal

def init_Normal(μ,σ,sum=True):
    
    def _init_Normal(nwalkers):
        
        values=np.random.randn(nwalkers,1)*σ+μ
        if sum:
            return np.sum(values,axis=1).reshape(nwalkers,1)
        else:
            return values
        
    return _init_Normal
    


def Uniform(mn,mx,sum=False):
    
    def _Uniform(x):
        try:
            N=len(x)
            
            if sum:
                if any(x<mn):
                    return -np.inf
                if any(x>mx):
                    return -np.inf
                
            values=np.log(1.0/(mx-mn))
            
            if sum:
                return values.sum()
            else:
                return values
            
        except TypeError:
            N=1

            if mn < x < mx:
                return np.log(1.0/(mx-mn))
            return -np.inf
        
        
    return _Uniform


def init_Uniform(mn,mx,sum=False):
    
    def _init_Uniform(nwalkers):
       
    
        values=np.random.rand(nwalkers,1)*(mx-mn)+mn
        if sum:
            return np.sum(values,axis=1).reshape(nwalkers,1)
        else:
            return values
    
        
    return _init_Uniform


def Exponential(scale,offset=0,sum=False):
    
    def _Exponential(x):
        try:
            N=len(x)
            
            if sum:
                if any(x<offset):
                    return -np.inf
                if any(x>mx):
                    return -np.inf
                
            values=-np.log(scale)-(x-offset)/scale 
            
            if sum:
                return values.sum()
            else:
                return values
            
        except TypeError:
            N=1

            if x<=offset:
                return -np.inf
            
            return -np.log(scale)-(x-offset)/scale            
            
        
        
    return _Exponential

# to init, we don't need exact match, just no illegal values
def init_Exponential(scale,offset=0,sum=False):
    
    def _init_Exponential(nwalkers):
        
        values=np.random.rand(nwalkers,1)*scale+offset
        if sum:
            return np.sum(values,axis=1).reshape(nwalkers,1)
        else:
            return values
        
    return _init_Exponential





def StudentT(df,mu,sd,sum=False):
    
    def _StudentT(x):
        
        t=(x-mu)/float(sd)
        
        try:
            N=len(x)            
        except TypeError:
            N=1

        values=N*(gammaln((df+1)/2.0)-0.5*log(df*np.pi)-gammaln(df/2.0)-np.log(sd))+(-(df+1)/2.0)*np.log(1+t**2/df)
        
        if any(np.isnan(values)):
            raise ValueError('NaN in StudentT',df,mu,sd)
            
        if sum:
            return np.sum(values)
        else:
            return values
        
        
    return _StudentT


# to init, we don't need exact match, just no illegal values
def init_StudentT(μ,σ,sum=False):
    
    def _init_StudentT(nwalkers):
        
        values=np.random.randn(nwalkers,1)*σ+μ
        if sum:
            return np.sum(values,axis=1).reshape(nwalkers,1)
        else:
            return values
        
    return _init_StudentT




def HalfNormal(μ,σ,sum=False):
    
    def _Normal(x):
        try:
            N=len(x)
            if any(x<0):
                return -np.inf
        except TypeError:
            N=1
            if x<0:
                return -np.inf
            
        values=-0.5*(x-μ)**2/σ**2 - 0.5*np.log(σ**2)-0.5*np.log(2*np.pi)
        if sum:
            return np.sum(values)
        else:
            return values
        
    return _Normal

# to init, we don't need exact match, just no illegal values
def init_HalfNormal(μ,σ,sum=False):
    
    def _init_HalfNormal(nwalkers):
        
        values=np.random.rand(nwalkers,1)*σ+μ
        if sum:
            return np.sum(values,axis=1).reshape(nwalkers,1)
        else:
            return values
        
    return _init_HalfNormal




def Jeffreys():
    
    def _Jeffreys(x):
        if x>0.0:
            values=-np.log(x)
        else:
            values=-np.inf

        return values    
        
    return _Jeffreys


def init_Jeffreys(sum=False):
    
    def _init_Jeffreys(nwalkers):
       
        values=np.random.rand(nwalkers,1)*2
        return values
    
        
    return _init_Jeffreys

# %% ../notebooks/01_mcmc.ipynb 9
class Parameter(object):
    
    def __init__(self,eqn,initial_value=None):
        self.eqn=eqn
        name,rest=eqn.split('~')
        self.name=name.strip()
        self.rest=rest.strip()
        self.length=1
        self.lower=-np.inf

        if 'Jeffreys' in self.rest:
            self.lower=0.0
            if initial_value is None:
                self.initial_value=1.0

        if 'Exponential' in self.rest:
            self.lower=0.0
            if initial_value is None:
                self.initial_value=1.0
                                
        if initial_value is None:
            self.initial_value=0.0
        else:
            self.initial_value=initial_value
        
        
    def __repr__(self):
        return self.name
        
    def __len__(self):
        return self.length
    
        
class StatsModel(object):
    def __init__(self):
        self.parameters={}
        self.data={}
        self.prior_parameters=[]
        self.likelihood_parameters=[]
        self.data_parameters=[]
        self.nwalkers=100
        self.sampler=None
        self.slices=None
        self.burn_percentage=25
        self.warnings=[]
        self.last_pos=None
        self.extra_params={}
    
    
    def add_data(self,**kwargs):
        self.data.update(**kwargs) 
        

    def extra(self,**kwargs):
        for key in kwargs:
            self.extra_params[key]=kwargs[key]
        
        
    def add(self,eqn):
        from io import StringIO
        import tokenize
        
        param=Parameter(eqn)
        
        # look for references to data
        tokens=[token[1] for token in tokenize.generate_tokens(StringIO(eqn).readline) if token[1]]
        found=False
        found_key=None
        for key in self.data:
            if key in tokens:
                found=True
                found_key=key
                
        if found:
            if tokens[0]==found_key:
                self.data_parameters.append(param)
                self.data_parameters[-1].length=len(self.data[found_key])   
            else:
                self.likelihood_parameters.append(param)
                self.likelihood_parameters[-1].length=1   
                self.parameters[param.name]=param
        else:
            self.prior_parameters.append(param)
            self.parameters[param.name]=param
                
                
        
    def __repr__(self):
        S="""
Parameters
----------
    %s
Extra
-----
    %s
Data
----
    %s
Prior
-----
    %s
Likelihood
----------
    %s
Data Parameters
---------------
    %s
        """ % (self.parameters,list(self.extra_params.keys()),list(self.data.keys()),
               [param.eqn for param in self.prior_parameters],
               [param.eqn for param in self.likelihood_parameters],
               [param.eqn for param in self.data_parameters],
              ) 
        
        return S
    
    def initialize(self):
        from collections import namedtuple
        self.make_func()
        
        names=','.join(self.parameters)
        slicetuple = namedtuple("slicetuple", names)
        lengths=cumsum([0]+[len(self.parameters[key]) for key in self.parameters])
        slices={}
        for i,key in enumerate(self.parameters):
            slices[key]=np.s_[lengths[i]:lengths[i+1]]
        self.slices=slicetuple(**slices)
        self.parameter_length=sum([len(self.parameters[key]) for key in self.parameters])
        
    def set_initial_values(self,method='ball',**kwargs):
        N=300
        ndim=self.parameter_length
        nwalkers=self.nwalkers

        if method=='ball':
            print("Setting Center Cluster...")
            center=zeros(ndim)
            for i,key in enumerate(self.parameters):
                center[self.slices.__getattribute__(key)]=self.parameters[key].initial_value
            
            self.last_pos=emcee.utils.sample_ball(center, 
                            0.05*center+1e-4, size=nwalkers)
            
            
            
            print("done.")
            
        elif method=='prior':
        
            self.sampler = emcee.EnsembleSampler(self.nwalkers, ndim, 
                                                 self._lnprior,args=(self.slices,self.extra_params,))

            pos=self._init_prior(nwalkers,ndim,self.data,self.slices,self.extra_params)
            
            
            # pos=np.zeros((nwalkers,ndim))
            # for i,key in enumerate(self.parameters):
            #     pos[:,self.slices[i]]=np.random.randn(nwalkers,len(self.parameters[key]))*10
            #     pos[:,self.slices[i]][pos[:,self.slices[i]]<=self.parameters[key].lower]=self.parameters[key].lower


            self.initial_pos=pos.copy()
            timeit(reset=True)
            print("Sampling Prior...")

            with warnings.catch_warnings(record=True) as warning_list:
                # Cause all warnings to always be triggered
                #warnings.simplefilter("always")
                # Call your function that issues a warning        
                self.sampler.run_mcmc(pos, N,**kwargs)
            
            self.warnings.extend(warning_list)
            self.burn_N=int(N*self.burn_percentage/100.0)

            print("Done.")
            print( timeit())
            
            # assign the median back into the simulation values
            self.samples = self.sampler.get_chain(discard=self.burn_N)
            #self.sampler.chain[:, :, :].reshape((-1, ndim))            
            self.median_values=np.percentile(self.samples.reshape((-1, ndim)),50,axis=0)

            self.last_pos=self.samples[-1,:,:]
            
            
        elif method=='samples':
            print("Samples")
            samples=self.samples.reshape((-1, ndim))
            lower,upper=np.percentile(samples, [16,84],axis=0)            
            subsamples=samples[((samples>=lower) & (samples<=upper)).all(axis=1),:]
            idx=np.random.randint(subsamples.shape[0],size=self.last_pos.shape[0])
            self.last_pos=subsamples[idx,:]            
        elif method=='median':            
            vals=self.median_values
            self.last_pos=emcee.utils.sample_ball(vals, 
                            0.05*vals+1e-4, size=self.nwalkers)
        else:
            raise ValueError("Unknown method: %s" % method)
            
        
    def burn(self,burn_percentage=None):
        if not burn_percentage is None:
            self.burn_percentage=burn_percentage
            
        if self.burn_percentage>1:
            self.burn_percentage/=100.0

        burnin = int(self.sampler.chain.shape[1]*self.burn_percentage)  # burn 25 percent
        ndim=self.parameter_length
        self.samples = self.sampler.chain[:, burnin:, :].reshape((-1, ndim))
        
    def run_mcmc(self,N,repeat=1,**kwargs):
        ndim=self.parameter_length
        nwalkers=self.nwalkers
                
        if self.last_pos is None:
            self.set_initial_values('prior')
        
        
        for i in range(repeat):        
            self.sampler = emcee.EnsembleSampler(self.nwalkers, ndim, self,)
            timeit(reset=True)
            if repeat==1:
                print("Running MCMC...")
            else:
                print("Running MCMC %d/%d..." % (i+1,repeat))

            self.sampler.run_mcmc(self.last_pos, N,**kwargs)
                                             
                                             
            self.burn_N=int(N*self.burn_percentage/100.0)
            self.samples = self.sampler.get_chain(discard=self.burn_N)
            
            print("Done.")
            print (timeit())

            if repeat>1:
                self.set_initial_values('samples')  # reset using the 16-84 percentile values from the samples


        # assign the median back into the simulation values
        self.median_values=np.percentile(self.samples.reshape((-1, ndim)),50,axis=0)
        theta=self.median_values

        #self.last_pos=self.sampler.chain[:,-1,:]
    
        
        
    def plot_chains(self,*args,**kwargs):
        import pylab as py
        
        if not args:
            args=[key for key in self.parameters if len(self.parameters[key])==1]
        else:
            for arg in args:
                assert arg in self.parameters
                
        L=sum([len(self.parameters[key]) for key in args])

        figsize=rcParams['figure.figsize']
        figsize[1]=5/8*figsize[0]*L  # make square
        figsize=kwargs.pop('figsize',figsize)
        
        print("figsize",figsize)
        fig, axes = py.subplots(len(args), 1, sharex=True, figsize=figsize)
        try:  # is it iterable?
            axes[0]
        except TypeError:
            axes=[axes]


        labels=[]
        count=0
        for key in args:
            s=self.slices.__getattribute__(key)
            sub_sample=self.samples[:, :, s]
            for i in range(len(self.parameters[key])):
                sample=sub_sample[:, :, i]
                ax=axes[count]
                ax.plot(sample, color="k", alpha=0.2,**kwargs)
                
                if len(self.parameters[key])==1:
                    ax.set_ylabel(f'{key}' )
                else:
                    ax.set_ylabel(f'{key}$_{i}$')


                
                count+=1
            
        
    def _lnposterior(self,θ):
        _value=0
        _value+=self._lnprior(θ,self.slices,self.extra_params)
        if not np.isfinite(_value):
            return -np.inf
        _value+=self._lnlikelihood(θ,self.data,self.slices,self.extra_params)
        
        return np.sum(_value)
    
    def __call__(self,θ):
        return self._lnposterior(θ)
    
    def percentiles(self,p=[16, 50, 84],*args):
        if not args:
            args=[key for key in self.parameters if len(self.parameters[key])==1]
        else:
            for arg in args:
                assert arg in self.parameters
        
        samples=self.samples.reshape((-1, ndim))
        self.median_values=np.percentile(samples,50,axis=0)
        
        result={}
        for key in args:
            s=self.slices.__getattribute__(key)
            sub_sample=samples[:,s]
            result[key]=np.percentile(sub_sample,[16,50,84],axis=0)
            
        return result
        
    def best_estimates(self,*args):
        return self.percentiles(p=[16, 50, 84],*args)


    def plot_distributions(self,*args,**kwargs):
        ndim=self.parameter_length
        
        if not args:
            args=[key for key in self.parameters if len(self.parameters[key])==1]
        
        samples=self.samples.reshape((-1, ndim))
        
        for key in self.parameters:
            idx=self.slices.__getattribute__(key)
            exec('%s=samples[:,idx]' % key)
        
        result=[]
        for key in args:
            values=eval(f"{key}")
            for i in range(values.shape[1]):
                sample=values[:, i].ravel()
            
                figure(figsize=(12,4))

                x,y=histogram(sample,bins=200,plot=False)
                plot(x,y,'.-')
                fill_between(x,y,facecolor='blue', alpha=0.2)

                HDI=np.percentile(sample, [2.5, 50, 97.5],axis=0)
                yl=gca().get_ylim()
                text((HDI[0]+HDI[2])/2, 0.15*yl[1],'95% HDI', ha='center', va='center',fontsize=12)
                plot(HDI,[yl[1]*.1,yl[1]*.1,yl[1]*.1],'k.-',linewidth=1)
                for v in HDI:
                    if v<0.005:
                        text(v, 0.05*yl[1],'%.3g' % v, ha='center', va='center', 
                             fontsize=12)
                    else:
                        text(v, 0.05*yl[1],'%.3f' % v, ha='center', va='center', 
                             fontsize=12)

                ylabel(r'$p(%s|{\rm data})$' % key)
                gca().set_xlabel(f'{key}' )
    
                result.append((key,i,HDI))
        
        return result
    

# %% ../notebooks/01_mcmc.ipynb 10
@patch
def make_func(self:StatsModel):
    s="def _lnprior(θ,slices,extra={}):\n"

    if self.extra_params:
        for key in self.extra_params:
            s+=f"    {key}=extra['{key}']\n"

    for param in self.prior_parameters:
        name=param.name
        s+=f"    {name}=θ[slices.{name}]\n" 

    s+="\n    _value=0\n\n"

    for param in self.prior_parameters:
        name=param.name
        rest=param.rest
        s+=f"    _value+={rest}({name})\n" 


    s+="\n    return _value\n"

    s+="\n\n"


    s+="def _init_prior(nwalkers,ndim,data,slices,extra={}):\n"
#     s+="\n    _value=None\n"
    
#     s+="\n    return _value\n"
#     s+="\n\n"

    if self.extra_params:
        for key in self.extra_params:
            s+=f"    {key}=extra['{key}']\n"
            
    for key in self.data:
        s+=f"    {key}=data['{key}']\n"
    s+="\n"
            

    s+=f"    _pos=np.zeros((nwalkers,ndim))\n" 

    for param in self.prior_parameters:
        name=param.name
        rest=param.rest        
        s+=f"    {name}=_pos[:,slices.{name}]=init_{rest}(nwalkers)\n" 

    for param in self.likelihood_parameters:
        name=param.name
        rest=param.rest
        s+=f"    {name}=_pos[:,slices.{name}]=init_{rest}(nwalkers)\n" 



    s+="\n    return _pos\n"

    s+="\n\n"




    s+="def _lnlikelihood(θ,data,slices,extra={}):\n"

    if self.extra_params:
        for key in self.extra_params:
            s+=f"    {key}=extra['{key}']\n"

    for key in self.data:
        s+=f"    {key}=data['{key}']\n"
    s+="\n"

    for param in self.prior_parameters:
        name=param.name
        s+=f"    {name}=θ[slices.{name}]\n" 
    s+="\n"
    for param in self.likelihood_parameters:
        name=param.name
        s+=f"    {name}=θ[slices.{name}]\n" 

    s+="\n    _value=0\n\n"

    for param in self.likelihood_parameters+self.data_parameters:
        name=param.name
        rest=param.rest
        s+=f"    _value+={rest}({name})\n"
        

    s+="\n    return _value.sum()\n"


    self.function_str=s

    
    
    exec(s)

    self._init_prior=locals()['_init_prior']
    self._lnprior=locals()['_lnprior']
    self._lnlikelihood=locals()['_lnlikelihood']

    return s


# %% ../notebooks/01_mcmc.ipynb 12
@patch
def P(self:StatsModel,S):
    ndim=self.parameter_length
    samples=self.samples.reshape((-1, ndim))
    
    for key in self.parameters:
        idx=self.slices.__getattribute__(key)
        exec('%s=samples[:,idx]' % key)

    N=float(np.prod(self.samples[:,0].shape))
    result=eval('np.sum(%s)/N' % S)
    return result

